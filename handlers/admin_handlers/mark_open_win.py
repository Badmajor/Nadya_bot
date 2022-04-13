from contextlib import suppress

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from data.constants import MONTHS
from data.loader import dp, dt, bot
from handlers.user_handlers.user_handlers import command_start_handler
from keyboards.callback_data import MonthsCallback, DayCallback, TimeCallback, StatusWinCallback, StartCallbackAdmin, \
    UserCallback
from keyboards.keyboards import keyboard_free_busy
from keyboards.keyboards_admin import keyboard_session_admin, keyboard_month_admin, keyboard_day_admin, \
    keyboard_start_admin, keyboard_session_with_name_admin, keyboard_chat_with_user
from states.ChoiceTime import ChoiceTimeAdmin
from utils.converters import get_time_str, get_datetime_str
from utils.database import PostString, clear_old_data, GetData


@dp.callback_query(StartCallbackAdmin.filter())
async def month_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: StartCallbackAdmin):
    btn = callback_data.action
    if btn == 'schedule':
        await clear_old_data(dt.month, dt.day)  # вычищает из базы предыдущие дни(придумать куда засунуть)
        await state.clear()
        await state.set_state(ChoiceTimeAdmin.admin_choice_month)
        await call.message.edit_text(f'Выбери месяц', reply_markup=keyboard_month_admin())
    if btn == 'today':
        enrolls = GetData()
        today = enrolls.get_schedule_today()
        if today:
            await call.message.edit_text(f'На сегодня записаны:', reply_markup=keyboard_session_with_name_admin(today))
        else:
            with suppress(TelegramBadRequest):
                await call.message.edit_text(f'На сегодня записей нет!', reply_markup=keyboard_start_admin())
        enrolls.close()
    else:
        await state.clear()
        await state.set_state(ChoiceTimeAdmin.admin_choice_month)
        await call.message.edit_text(f'Выбери месяц', reply_markup=keyboard_month_admin())
    await call.answer()


@dp.callback_query(MonthsCallback.filter(), state=ChoiceTimeAdmin.admin_choice_month)
async def day_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: MonthsCallback):
    m = callback_data.num_month
    month = m if m < 13 else m % 12
    year = dt.year if m < 12 else dt.year + 1
    data = {'year': year, 'month': month}
    await state.set_data(data)
    await state.set_state(ChoiceTimeAdmin.admin_choice_date)
    await call.message.edit_text(f'{MONTHS[month]}\n'
                                 f'А теперь выбери день',
                                 reply_markup=keyboard_day_admin(m))
    await call.answer()


@dp.callback_query(DayCallback.filter(), state=ChoiceTimeAdmin.admin_choice_date)
async def time_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: DayCallback):
    day = callback_data.num_day
    data = await state.get_data()
    month = data['month']
    data['day'] = day
    await state.set_data(data)
    await state.set_state(ChoiceTimeAdmin.admin_choice_time)
    await call.message.edit_text(f'{MONTHS[month % 12 - 1]}, {day}-е\n'
                                 f'А теперь выбери окно',
                                 reply_markup=keyboard_session_admin(data))
    await call.answer()


@dp.callback_query(TimeCallback.filter(), state=ChoiceTimeAdmin.admin_choice_time)
async def status_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: TimeCallback):
    time = callback_data.start_time
    data = await state.get_data()
    year, month, day = data['year'], data['month'], data['day']
    data['time'] = time
    enroll = GetData(year, month, day, time)
    s = f'Запись: {enroll.string()[7]}' if enroll.string() else 'Что будем делать?'
    await state.set_data(data)
    await state.set_state(ChoiceTimeAdmin.admin_post_data_db)
    await call.message.edit_text(f'{get_datetime_str(year, month, day, time)}\n'
                                 f'{s}',
                                 reply_markup=keyboard_free_busy())
    await call.answer()


@dp.callback_query(StatusWinCallback.filter(), state=ChoiceTimeAdmin.admin_post_data_db)
async def post_in_db_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: StatusWinCallback):
    status = callback_data.status
    data = await state.get_data()
    time = (data['year'], data['month'], data['day'], data['time'])
    s = 'Свободно' if status else 'Занято'
    await call.message.edit_text(f'{get_datetime_str(*time)}\n'
                                 f'{s}')
    enroll = GetData(*time)
    win = PostString(*time, status=status)
    if enroll.string():
        data = enroll.string()
        if data[7]:
            await bot.send_message(chat_id=data[5],
                                   text=f'Ваша запись на {time[2]}.{time[1]}.{time[0]} в {get_time_str(time[3])} '
                                        f'отменена')
        win.enroll()
        enroll.close()
    else:
        win.make_win()
        win.close()
        enroll.close()
    await state.clear()
    await command_start_handler(message=call.message)
    await call.answer()


@dp.callback_query(UserCallback.filter())
async def post_in_db_for_open_win(call: CallbackQuery, callback_data: UserCallback):
    tg_id, time, name = callback_data.tg_id, callback_data.time, callback_data.name
    await call.message.edit_text(f'{name} в {get_time_str(time)}',
                                 reply_markup=keyboard_chat_with_user(tg_id))
    await call.answer()
