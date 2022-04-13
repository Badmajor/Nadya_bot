import datetime
import math

from data.config import DAY_OFF, HOLIDAYS
from data.loader import dt
from utils.converters import get_time_str
from utils.database import GetData


def check_month(month: int, year: int) -> int:
    """
    Возвращает количество дней в месяце
    """
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 28 if year % 4 else 2


def check_date(year: int, month: int, day: int) -> bool:
    """
    Проверяет день на праздник и выходной, если не находит его в списках выходных и праздников возвращает True
    :param year:
    :param month:
    :param day:
    :return:
    """
    date = datetime.date(year, month, day)
    day_week = date.isoweekday()
    if day_week in DAY_OFF:
        return False
    if (month, day) in HOLIDAYS:
        return False
    return True


def check_enrolls_user(tg_id: int) -> list[tuple]:
    """
    Возвращает будущие записи юзера списком кортежей (год, месяц, день, время: float,
    статус, id телеграмм, телефон, Имя).

    :param tg_id:
    :return:
    """
    enrolls_list = []
    enrolls = GetData(tg_id=tg_id)
    data = enrolls.string()
    for i in data:
        year, month, day, time, status, tg_id, phone, name = i
        if dt.replace(year=year, month=month, day=day, hour=math.ceil(time)) >= dt:
            enrolls_list.append(i)
    enrolls.close()
    return enrolls_list


def check_enrolls_date(month: int, day: int) -> list:
    """
    Возвращает будущие записи юзера списком кортежей (год, месяц, день, время: float,
    статус, id телеграмм, телефон, Имя).
    """
    enrolls_list = []
    enrolls = GetData(w_month=month, w_day=day)
    data = enrolls.get_schedule_day()
    for i in data:
        year, month, day, time, status, tg_id, phone, name = i
        enrolls_list.append(f'в {get_time_str(time)} - {name}')
    enrolls.close()
    return enrolls_list
