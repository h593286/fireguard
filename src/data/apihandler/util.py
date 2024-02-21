
import datetime


def format_date(dt: datetime.datetime):
    return dt.strftime('%Y-%m-%d')


def format_period(start: datetime.datetime, end: datetime.datetime):
    start_date = format_date(start)

    end_date = format_date(end)

    timeperiod = f'{start_date}/{end_date}'

    return timeperiod

