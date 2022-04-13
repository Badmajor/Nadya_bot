from aiogram.dispatcher.filters.callback_data import CallbackData


class StartCallback(CallbackData, prefix='start'):
    action: str


class StartCallbackAdmin(CallbackData, prefix='start_admin'):
    action: str


class MonthsCallback(CallbackData, prefix='month'):
    num_month: int


class DayCallback(CallbackData, prefix='day'):
    num_day: int


class TimeCallback(CallbackData, prefix='time'):
    start_time: float


class UserCallback(CallbackData, prefix='tg_id'):
    tg_id: int
    time: float
    name: str


class CancelCallback(CallbackData, prefix='cancel'):
    """
    True возвращает на главную,
    False на предыдущий стейт
    """
    home: bool


class StatusWinCallback(CallbackData, prefix='win'):
    status: bool


class SessionCallback(CallbackData, prefix='date'):
    year: int
    month: int
    day: int
    time: float
