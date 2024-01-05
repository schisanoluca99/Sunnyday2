import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error
import sqlite3

from keras.models import Sequential, load_model
from keras.layers import *

class Model:

    def __init__(self, table_name):
        self.table_name = table_name

    def extract_df(self):
        conn = sqlite3.connect('DATA/DATI.db')
        df = pd.read_sql(f'SELECT * FROM {self.table_name}', conn, parse_dates={'time':{'format':'%Y-%m-%d'}})
        conn.close()
        return df.set_index('time')

    def train_test(self, date='2021-07-27'):
        df = self.extract_df().dropna()
        train = df[df.index <= date]
        test = df[df.index > date]

        return (train, test)

    def _scale_df(self):
        train, test = self.train_test()
        scaler = MinMaxScaler(feature_range=(0,1))
        sc = scaler.fit(train)
        train_scaled = sc.transform(train)
        test_scaled = sc.transform(test)

        return (train_scaled, test_scaled)

    def _create_X_Y(self, T=7):
        series_train = self.train_test()[0].to_numpy()
        series_test = self.train_test()[1].to_numpy()
        series_tot = np.vstack((series_train, series_test)) #prendo anche i dati nel mezzo tra train e test
        x_train = []
        x_test = []
        y_train = []
        y_test = []

        for i in range(len(series_train) - T):
            x = series_train[i:i+T]
            x_train.append(x)
            y = series_train[i+T]
            y_train.append(y)

        for i in range(len(series_train) - T, len(series_train)):
            """Così gestisco i dati tra il train e il test, per non perderne neanche uno"""
            x = series_tot[i:i+T]
            x_test.append(x)
            y = series_tot[i+T]
            y_test.append(y)

        for i in range(len(series_test) - T):
            x = series_test[i:i+T]
            x_test.append(x)
            y = series_test[i+T]
            y_test.append(y)

        x_train = np.array(x_train) # length, T osservazioni, 9 colonne: totale 3 dimensioni
        x_test = np.array(x_test)
        y_train = np.array(y_train) # length, 9 colonne: totale 2 dimensioni
        y_test = np.array(y_test)

        return (x_train, y_train), (x_test, y_test)

    def define_variable_response(self, y_label='temperature_2m_max'):
        df = self.extract_df()
        pos_y = df.columns.to_list().index(y_label)

        return pos_y

    def train_model(self, y_label):
        x_train, y_train = self._create_X_Y()[0]
        y_train = y_train[:,self.define_variable_response(y_label)]

        model = Sequential()
        model.add(LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
        model.add(LSTM(20, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(loss='mse',
                      optimizer='adam',
                      metrics=['mean_absolute_error'])

        model.fit(x_train, y_train, epochs=20, batch_size=64)
        return model.save('MODELS/myModel.keras')

    def test_model(self):
        x_test, y_test = self._create_X_Y()[1]
        y_test = y_test[:, self.define_variable_response()]
        model = load_model('MODELS/myModel.keras')

        test_prediction = model.predict(x_test)

        return (y_test, test_prediction)

    def metrics(self, metrics_list: list):
        y_test, prediction = self.test_model()
        metrics = {}
        if 'mean_squared_error' or 'mse' in metrics_list:
            metrics['mean_squared_error'] = mean_squared_error(y_test, prediction)

        if 'mean_absolute_error' or 'mae' in metrics_list:
            metrics['mean absoulte error'] = mean_absolute_error(y_test, prediction)

        if 'mean_squared_log_error' or 'msle' in metrics_list:
            metrics['mean_squared_log_error'] = mean_squared_log_error(y_test, prediction)

        return pd.DataFrame(metrics, index=['Metrics'])

    def create_df_result(self):
        y_test = self.test_model()[0].reshape(-1,1)
        prediction = self.test_model()[1]

        united = np.hstack((y_test, prediction))
        df = pd.DataFrame(united, columns=['Test', 'Prediction'])

        return df

if __name__ == '__main__':
    roma = Model('Roma')
    roma.train_model('temperature_2m_min')