
import datetime

# Time format class, maybe more tools later
def format_date(dt: datetime.datetime | datetime.date):
    return dt.strftime('%Y-%m-%d')


def format_period(start: datetime.datetime, end: datetime.datetime):
    start_date = format_date(start)

    end_date = format_date(end)

    timeperiod = f'{start_date}/{end_date}'

    return timeperiod

