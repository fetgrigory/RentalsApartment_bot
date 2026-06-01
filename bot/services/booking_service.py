from datetime import datetime, timedelta


def calculate_days(current: int, delta: int, min_days: int = 1) -> int:
    return max(current + delta, min_days)


def calculate_price(price_per_day: int, days: int) -> int:
    return price_per_day * days


def get_dates(days: int):
    start = datetime.now().date()
    end = start + timedelta(days=days)
    return start, end
