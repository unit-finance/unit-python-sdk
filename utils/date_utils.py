from datetime import date, datetime


def to_datetime(dt: str):
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")


def to_date(d: str):
    return date.fromisoformat(d)


def to_date_str(d: date):
    return d.strftime("%Y-%m-%d")
