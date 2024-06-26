
import datetime

# Time format class, maybe more tools later
def format_date(dt: datetime.datetime | datetime.date):
    return dt.strftime('%Y-%m-%d')

def format_datetime(dt: datetime.datetime):
    return dt.strftime('%Y-%m-%dT%h:%M:%s%Z')

def format_period(start: datetime.datetime | datetime.date, end: datetime.datetime | datetime.date):
    start_date = format_date(start)

    end_date = format_date(end)

    timeperiod = f'{start_date}/{end_date}'

    return timeperiod

