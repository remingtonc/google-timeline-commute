import json
import pdb
from .address import get_coordinates
from geopy.distance import lonlat, distance

class LocationHistory:

    def __init__(self, file_path, api_key):
        self.file_path = file_path
        self.raw = self.load_from_json(self.file_path)
        self.api_key = api_key
    
    def load_from_json(self, file_path):
        content = None
        with open(file_path, 'r') as file_fd:
            content = json.load(file_fd)
        return content
    
    def get_timestamps_by_address(self, address, radius=1):
        addr_latitude, addr_longitude = get_coordinates(address, self.api_key)
        return addr_latitude, addr_longitude, self.get_timestamps_by_coordinates(addr_latitude, addr_longitude, radius)
    
    def get_timestamps_by_coordinates(self, latitude, longitude, radius=1):
        timestamps = []
        for location in self.raw['locations']:
            timestamp = int(int(location['timestampMs']) / 1000)
            loc_latitude = location['latitudeE7'] / 1e7
            loc_longitude = location['longitudeE7'] / 1e7
            coord_distance = distance(
                lonlat(longitude, latitude),
                lonlat(loc_longitude, loc_latitude)
            ).miles
            if radius >= coord_distance:
                timestamps.append(timestamp)
        return sorted(timestamps)
