import pytz

UTC = pytz.utc
IST = pytz.timezone("Asia/Kolkata")

def ist_to_utc(dt):
    return IST.localize(dt).astimezone(UTC)

def utc_to_ist(dt):
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    return dt.astimezone(IST)
