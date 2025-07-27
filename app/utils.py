from datetime import datetime
import pytz

def to_utc(local_dt, tz='Asia/Kolkata'):
    local = pytz.timezone(tz)
    return local.localize(local_dt).astimezone(pytz.utc)

def from_utc(utc_dt, tz='Asia/Kolkata'):
    local = pytz.timezone(tz)
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(local)
