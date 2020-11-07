from datetime import datetime, timedelta


def is_recent(d: datetime) -> bool:
    now = datetime.now()
    return now - timedelta(seconds=1) <= d <= now
