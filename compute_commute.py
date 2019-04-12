#!/usr/bin/env python
import json
import statistics
import logging
from timeline_commute import LocationHistory
from timeline_commute import commute

def load_config(file_path='config.json'):
    config = None
    with open(file_path, 'r') as config_fd:
        config = json.load(config_fd)
    return config

def save_config(config, file_path='config.json'):
    with open(file_path, 'w') as config_fd:
        json.dump(config, config_fd)

def main():
    config = load_config()
    my_location_history = LocationHistory('Location History.json', config['api_key'])
    home_latitude, home_longitude, work_latitude, work_longitude = (None,)*4
    home_timestamps, work_timestamps = (None,)*2
    if not set(['home_latitude', 'home_longitude']).issubset(set(config.keys())):
        home_latitude, home_longitude, home_timestamps = my_location_history.get_timestamps_by_address(config['home'])
        config['home_latitude'] = home_latitude
        config['home_longitude'] = home_longitude
    else:
        home_latitude = config['home_latitude']
        home_longitude = config['home_latitude']
        home_timestamps = my_location_history.get_timestamps_by_coordinates(home_latitude, home_longitude)
    if not set(['work_latitude', 'work_longitude']).issubset(set(config.keys())):
        work_latitude, work_longitude, work_timestamps = my_location_history.get_timestamps_by_address(config['home'])
        config['work_latitude'] = work_latitude
        config['work_longitude'] = work_longitude
    else:
        work_latitude = config['work_latitude']
        work_longitude = config['work_longitude']
        work_timestamps = my_location_history.get_timestamps_by_coordinates(work_latitude, work_longitude)
    save_config(config)
    home_work_commutes, work_home_commutes = commute.parse_commutes(home_timestamps, work_timestamps)
    work_commute_times = commute.parse_commute_times(home_work_commutes)
    home_commute_times = commute.parse_commute_times(work_home_commutes)
    logging.info('Work commute average: %d', statistics.mean(work_commute_times))
    logging.info('Home commute average: %d', statistics.mean(home_commute_times))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
