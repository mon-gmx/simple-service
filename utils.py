from datetime import UTC, datetime


def get_now_time() -> object:
    """Return a timestamp in UTC timezone"""
    return datetime.now(UTC)
