from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.constants import MONTHS
from data.loader import dt
from keyboards.callback_data import TimeCallback, MonthsCallback, DayCallback, StartCallbackAdmin, CancelCallback, \
    UserCallback
from keyboards.default_btns import default_btns
from utils.check_data import check_month, check_date
from utils.converters import get_time_str
from utils.database import GetData
from utils.get_sessions import get_session_btn, get_time_float


def keyboard_start_admin() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    schedule_btn = InlineKeyboardButton(text='Редактировать график',
                                        callback_data=StartCallbackAdmin(action='schedule').pack())
    today_btn = InlineKeyboardButton(text='Кто сегодня?',
                                     callback_data=StartCallbackAdmin(action='today').pack())
    view_day_btn = InlineKeyboardButton(text='Посмотреть запись на день',
                                        callback_data=StartCallbackAdmin(action='view').pack())
    keyboard.add(schedule_btn)
    keyboard.add(today_btn)
    keyboard.row(view_day_btn)
    return keyboard.as_markup()


def keyboard_month_admin() -> InlineKeyboardMarkup:
    month = dt.month
    keyboard = InlineKeyboardBuilder()
    for i in range(3):
        keyboard.add(InlineKeyboardButton(
            text=MONTHS[(month + i) % 12 - 1],
            callback_data=MonthsCallback(
                num_month=month + i).pack()
        ))
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_day_admin(m: int) -> InlineKeyboardMarkup:
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
        if check_date(year, month, day + i):
            keyboard.add(InlineKeyboardButton(
                text=day + i,
                callback_data=DayCallback(
                    num_day=day + i).pack()
            ))
    keyboard.adjust(5)
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_session_admin(data) -> InlineKeyboardMarkup:
    y, m, d = data.values()
    session_status = GetData(y, m, d)
    list_sessions = get_session_btn() if (m, d) != (dt.month, dt.day) else get_session_btn(today=True)
    keyboard = InlineKeyboardBuilder()
    for i in range(len(list_sessions) - 1):
        session_status.w_time = get_time_float(list_sessions[i])
        emoji_dict = {1: '🆓', 0: '✅', -1: '❌'}
        keyboard.add(InlineKeyboardButton(
            text=f'{emoji_dict[session_status.check_status()]}{list_sessions[i]}-{list_sessions[i + 1]}',
            callback_data=TimeCallback(
                start_time=get_time_float(list_sessions[i])).pack()
        ))
    session_status.close()
    keyboard.adjust(3)
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_session_with_name_admin(sessions: list[tuple]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for i in sessions:
        keyboard.row(InlineKeyboardButton(
            text=f'в {get_time_str(i[3])} {i[7]}',
            callback_data=UserCallback(
                tg_id=i[5], time=i[3], name=i[7]).pack()))
    keyboard.row(*default_btns)
    return keyboard.as_markup()


def keyboard_chat_with_user(tg_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Написать клиенту', url=f'tg://user?id={tg_id}'))
    keyboard.add(InlineKeyboardButton(text='В меню', callback_data=CancelCallback(home=True).pack()))
    return keyboard.as_markup()
