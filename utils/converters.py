from data.constants import MONTHS


def get_time_float(time: str) -> float:
    a = time.split(':')
    return int(a[0]) + int(a[1]) / 60


def get_time_str(time: float) -> str:
    s_hour = str(int(time))
    s_minutes = '00' if not time % 1 else str(int(60 * (time % 1)))
    return f'{s_hour}:{s_minutes}'


def get_datetime_str(year: int, month: int, day: int, time: float, *args, **kwargs) -> str:
    return f'{day} {MONTHS[month-1]} {year} в {get_time_str(time)}'
