from datetime import datetime
from zoneinfo import ZoneInfo


def current_date():
    date_format    = "%Y-%m-%d %H:%M:%S"
    current_date   = datetime.now().strftime(date_format)
    return current_date