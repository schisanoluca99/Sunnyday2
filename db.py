import sqlite3
from sqlalchemy import create_engine

#with open('DATA/DATI.db', 'w') as f:
#    print('Creato il file')

def create_table(database, table_name):
    connection = sqlite3.connect(f'DATA/{database}.db')
    connection.execute(f"""
        CREATE TABLE "{table_name}"(
            'time' NVARCHAR(255),
            'weather_code' FLOAT,
            'temperature_2m_max' FLOAT,
            'temperature_2m_min' FLOAT,
            'precipitation_sum' FLOAT,
            'rain_sum' FLOAT,
            'snowfall_sum' FLOAT,
            'precipitation_hours' FLOAT,
            'wind_speed_10m_max' FLOAT,
            'shortwave_radiation_sum' FLOAT
        )
        """)
    connection.commit()
    connection.close()

def insert_value(df, database, table_name):
    engine = create_engine(f'sqlite:///DATA/{database}.db', echo=False)
    df.to_sql(f'{table_name}', con=engine, if_exists='append', index=False)

def delete_table(database, table_name):
    connection = sqlite3.connect(f'DATA/{database}.db')
    connection.execute(f"""
            DROP TABLE "{table_name}" """)
    connection.commit()
    connection.close()

def select_All(database, table_name):
    connection = sqlite3.connect(f'DATA/{database}.db')
    cursor = connection.cursor()

    cursor.execute(f"""
    SELECT * FROM "{table_name}"
    """)
