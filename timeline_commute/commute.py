from datetime import datetime
import logging

def parse_commutes(home_timestamps, work_timestamps):
    home_work_commutes = []
    work_home_commutes = []
    home_dates = __parse_timestamps(home_timestamps)
    logging.info(home_dates)
    work_dates = __parse_timestamps(work_timestamps)
    logging.info(work_dates)
    commute_dates = home_dates.keys() & work_dates.keys()
    logging.info(commute_dates)
    for commute_date in commute_dates:
        if len(home_dates[commute_date]) != len(work_dates[commute_date]):
            logging.error(
                '%s home (%d) and work (%d) instances do not match!',
                commute_date,
                len(home_dates[commute_date]),
                len(work_dates[commute_date])
            )
        home_work_commute = (
            sorted(home_dates[commute_date])[0],
            sorted(work_dates[commute_date])[0]
        )
        home_work_commutes.append(home_work_commute)
        work_home_commute = (
            sorted(work_dates[commute_date], reverse=True)[0],
            sorted(work_dates[commute_date], reverse=True)[0]
        )
        work_home_commutes.append(work_home_commute)
    return home_work_commutes, work_home_commutes

def parse_commute_times(commutes):
    commute_times = []
    for commute in commutes:
        start_time, end_time = (commute[0], commute[1]) if commute[0] > commute[1] else (commute[1], commute[0])
        commute_times.append(end_time - start_time)
    return commute_times

def __parse_timestamps(timestamps):
    dated_timestamps = {}
    for timestamp in dated_timestamps:
        timestamp_dated = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        if timestamp_dated not in dated_timestamps.keys():
            dated_timestamps[timestamp_dated] = []
        dated_timestamps[timestamp_dated].append(timestamp_dated)
    return dated_timestamps
