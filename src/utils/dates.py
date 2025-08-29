from datetime import datetime, timedelta
from dateutil import tz

def now_tz(tz_name: str = "Europe/Madrid") -> datetime:
    return datetime.now(tz.gettz(tz_name))

def last_24h_window(tz_name: str = "Europe/Madrid"):
    """Devuelve (start, end) redondeados a minuto: (ahora-24h, ahora)."""
    now = now_tz(tz_name)
    start = (now - timedelta(hours=24)).replace(minute=0, second=0, microsecond=0)
    end   =  now.replace(minute=59, second=0, microsecond=0)
    return start, end, now

def partition_str(dt: datetime) -> str:
    """YYYY-MM-DD para usar en partition_date=..."""
    return dt.strftime("%Y-%m-%d")

def timestamp_str(dt: datetime) -> str:
    """YYYYMMDD_HHMM para nombre de archivo."""
    return dt.strftime("%Y%m%d_%H%M")