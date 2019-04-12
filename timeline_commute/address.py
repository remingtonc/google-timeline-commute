import requests

COORDINATE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'

def get_coordinates(address, api_key):
    if not api_key:
        raise Exception('%s is not valid API key!', api_key)
    parsed_address = address.replace(' ', '+')
    query_url = COORDINATE_URL.format(address=parsed_address, api_key=api_key)
    response = requests.get(query_url)
    response_json = response.json()
    location_data = response_json['results'][0]['geometry']['location']
    latitude = location_data['lat']
    longitude = location_data['lng']
    return latitude, longitude
