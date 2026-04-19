from datetime import date
from calendar import monthrange


def current_month_range() -> tuple[date, date]:
    """Zwraca (pierwszy_dzien_biezacego_miesiaca, ostatni_dzien)."""
    today = date.today()
    first = today.replace(day=1)
    last = today.replace(day=monthrange(today.year, today.month)[1])
    return first, last


def month_range(year: int, month: int) -> tuple[date, date]:
    """Zwraca (pierwszy_dzien, ostatni_dzien) dla podanego miesiąca."""
    first = date(year, month, 1)
    last = date(year, month, monthrange(year, month)[1])
    return first, last
