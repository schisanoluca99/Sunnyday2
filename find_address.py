from geopy.geocoders import Nominatim

def get_lan_long(city):
    loc = Nominatim(user_agent="Geopy Library")
    getLoc = loc.geocode(city)
    return (getLoc.latitude, getLoc.longitude)

if __name__ == '__main__':
    print(get_lan_long('Roma'))