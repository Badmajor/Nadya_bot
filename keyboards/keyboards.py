from contextlib import suppress

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.constants import MONTHS
from data.loader import dt
from keyboards.callback_data import StatusWinCallback, MonthsCallback, DayCallback, TimeCallback, \
    SessionCallback, StartCallback
from keyboards.default_btns import default_btns
from utils.check_data import check_month, check_date
from utils.converters import get_datetime_str
from utils.database import GetData
from utils.get_sessions import get_session_btn, get_time_float


def keyboard_start(user_id: int) -> InlineKeyboardMarkup:
    """ user_id задел на перспективу, жопой чую пригодится"""
    keyboard = InlineKeyboardBuilder()
    enroll_btn = InlineKeyboardButton(text='Записаться', callback_data=StartCallback(action='enroll').pack())
    cancel_btn = InlineKeyboardButton(text='Отменить запись', callback_data=StartCallback(action='cancel').pack())
    remind_btn = InlineKeyboardButton(text='Когда у меня запись?', callback_data=StartCallback(action='remind').pack())
    keyboard.add(enroll_btn)
    keyboard.add(cancel_btn)
    keyboard.row(remind_btn)
    return keyboard.as_markup()


def keyboard_free_busy() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    free_btn = InlineKeyboardButton(text='Свободно', callback_data=StatusWinCallback(status=True).pack())
    busy_btn = InlineKeyboardButton(text='Занято', callback_data=StatusWinCallback(status=False).pack())
    keyboard.add(free_btn)
    keyboard.add(busy_btn)
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_month() -> InlineKeyboardMarkup:
    month = dt.month
    keyboard = InlineKeyboardBuilder()
    for i in range(3):
        w_month = month + i
        check_m = GetData(w_month=w_month)
        if check_m.check_month():
            keyboard.add(InlineKeyboardButton(
                text=MONTHS[w_month % 12 - 1],
                callback_data=MonthsCallback(
                    num_month=w_month).pack()
            ))
        check_m.close()
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_day(m: int) -> InlineKeyboardMarkup:
    year = dt.year if m < 12 else dt.year + 1
    month = m if m < 13 else m % 12
    if month != dt.month:
        day = 1
        count = check_month(month, year)
    else:
        day = dt.day
        count = check_month(month, year) - day + 1
    keyboard = InlineKeyboardBuilder()
    for i in range(count):
        w_day = day + i
        check_d = GetData(w_month=month, w_day=w_day)
        if check_d.check_day():
            if check_date(year, month, w_day):
                keyboard.add(InlineKeyboardButton(
                    text=w_day,
                    callback_data=DayCallback(
                        num_day=w_day).pack()
                ))
        check_d.close()
    keyboard.adjust(5)
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_free_session_user(data: dict) -> InlineKeyboardMarkup:
    y, m, d = data.values()
    session_status = GetData(y, m, d)
    list_sessions = get_session_btn() if (m, d) != (dt.month, dt.day) else get_session_btn(today=True)
    keyboard = InlineKeyboardBuilder()
    for i in range(len(list_sessions)-1):
        session_status.w_time = get_time_float(list_sessions[i])
        if session_status.check_status() == 1:
            keyboard.add(InlineKeyboardButton(
                text=f'{list_sessions[i]}-{list_sessions[i + 1]}',
                callback_data=TimeCallback(
                    start_time=get_time_float(list_sessions[i])).pack()
            ))
    session_status.close()
    keyboard.adjust(4)
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_enrolls_user(data: list[tuple]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for i in data:
        year, month, day, time, status, tg_id, phone, name = i
        session_btn = InlineKeyboardButton(
            text=f'{get_datetime_str(*i)}',
            callback_data=SessionCallback(year=year, month=month, day=day, time=time).pack()
            )
        keyboard.row(session_btn)
    keyboard.row(*default_btns)
    return keyboard.as_markup()
