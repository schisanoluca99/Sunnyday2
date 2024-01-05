from sunnyday2 import Weather
from db import create_table, insert_value
from find_address import get_lan_long

lista_citta = ['Lisbona', 'Londra', 'Vienna', 'Roma']

for citta in lista_citta:
    lat = get_lan_long(citta)[0]
    lon = get_lan_long(citta)[1]
    weather = Weather(lat, lon)
    df = weather.prepare_df()

    create_table('DATI', citta)
    insert_value(df, 'DATI', citta)
