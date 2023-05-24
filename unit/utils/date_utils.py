from datetime import date, datetime


def to_datetime(dt: str):
    if dt is None:
        return None

    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")

def from_datetime(dt: datetime):
    return dt.isoformat(timespec='milliseconds') + "Z"

def to_date(d: str):
    if d is None:
        return None

    return date.fromisoformat(d)


def to_date_str(d: date):
    return d.strftime("%Y-%m-%d")


def to_year_str(d: date):
    if type(d) is not date:
        return None

    return d.strftime("%Y")