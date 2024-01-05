import requests
import pandas as pd
import numpy as np
from keras.models import load_model
from find_address import get_lan_long
"""
https://open-meteo.com/en/docs/historical-weather-api
weather_code
temperature_2m_max
temperature_2m_min
precipitation_sum
rain_sum
snowfall_sum
precipitation_hours
wind_speed_10m_max
wind_gusts_10m_max
shortwave_radiation_sum
"""

class Weather:

    def __init__(self, city=None, lat=None, lon=None, start_date='2016-01-01', end_date='2023-12-30'):
        if city:
            lat = get_lan_long(city)[0]
            lon = get_lan_long(city)[1]
            url = (f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}'
                   f'&start_date={start_date}&end_date={end_date}&'
                   f'daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,'
                   f'snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,'
                   f'shortwave_radiation_sum')
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = (f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}'
                   f'&start_date={start_date}&end_date={end_date}&'
                   f'daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,'
                   f'snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,'
                   f'shortwave_radiation_sum')
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError('Provide city or lat and lon arguments')

        try:
            if self.data['error']:
                raise ValueError(self.data['reason'])
        except:
            pass

    def prepare_df(self):
        df = pd.DataFrame(self.data['daily'])
        return df

    def forcast_next_day_max_temp(self, model_path, T=7):
        """Modello allenato sui 7 giorni precedenti"""
        df = self.prepare_df().dropna()[-T:].set_index('time')
        x = df.to_numpy()
        model = load_model(model_path)
        prediction_tomorrow = model.predict(x.reshape(1, T, x.shape[1]), verbose=0) #una sola osservazione passata, step=T, 9 colonne

        return prediction_tomorrow

    def forcast_next_day_min_temp(self, model_path, T=7):
        df = self.prepare_df().dropna()[-T:].set_index('time')
        x = df.to_numpy()
        model = load_model(model_path)
        prediction_tomorrow = model.predict(x.reshape(1, T, x.shape[1]), verbose=0) #una sola osservazione passata, step=T, 9 colonne

        return prediction_tomorrow


if __name__ == '__main__':
    weather = Weather(city='Roma', end_date='2024-01-01')
    #print(weather.prepare_df())
    print('MAX TEMP PREDICTION: ', weather.forcast_next_day_max_temp('MODELS/myModel_max_temp.keras')[0][0])
    print('MIN TEMP PREDICTION: ', weather.forcast_next_day_max_temp('MODELS/myModel_min_temp.keras')[0][0])
