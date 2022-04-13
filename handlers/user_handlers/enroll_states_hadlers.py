from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMIN
from data.constants import MONTHS
from data.loader import dp, dt, bot
from keyboards.callback_data import MonthsCallback, DayCallback, TimeCallback
from keyboards.keyboards import keyboard_day, keyboard_free_session_user, keyboard_start
from keyboards.keyboards_admin import keyboard_chat_with_user
from states.ChoiceTime import ChoiceTimeUser
from utils.converters import get_datetime_str
from utils.database import PostString


@dp.callback_query(MonthsCallback.filter(), state=ChoiceTimeUser.user_choice_month)
async def day_for_enroll(call: CallbackQuery, state: FSMContext, callback_data: MonthsCallback):
    m = callback_data.num_month
    month = m if m < 13 else m % 12
    year = dt.year if m < 12 else dt.year + 1
    data = {'year': year, 'month': month}
    await state.set_data(data)
    await state.set_state(ChoiceTimeUser.user_choice_date)
    await call.message.edit_text(f'{MONTHS[month]}\n'
                                 f'А теперь выбери день',
                                 reply_markup=keyboard_day(m))
    await call.answer()


@dp.callback_query(DayCallback.filter(), state=ChoiceTimeUser.user_choice_date)
async def time_for_enroll(call: CallbackQuery, state: FSMContext, callback_data: DayCallback):
    day = callback_data.num_day
    data = await state.get_data()
    month = data['month']
    data['day'] = day
    await state.set_data(data)
    await state.set_state(ChoiceTimeUser.user_choice_time)
    await call.message.edit_text(f'{MONTHS[month % 12 - 1]}, {day}-е\n'
                                 f'А теперь выбери время',
                                 reply_markup=keyboard_free_session_user(data))
    await call.answer()


@dp.callback_query(TimeCallback.filter(), state=ChoiceTimeUser.user_choice_time)
async def post_in_db_for_open_win(call: CallbackQuery, state: FSMContext, callback_data: TimeCallback):
    time = callback_data.start_time
    data = await state.get_data()
    year, month, day = data['year'], data['month'], data['day']
    user = call.from_user
    name, tg_id = user.full_name, user.id
    status = 0
    await call.answer(f'✅ Записала\n'
                      f'{get_datetime_str(year, month, day, time)}', show_alert=True)
    await call.message.edit_text(f'✅ Записала\n'
                                 f'{get_datetime_str(year, month, day, time)}',
                                 reply_markup=keyboard_start(tg_id)
                                 )
    enroll = PostString(w_year=year, w_month=month, w_day=day, w_time=time, status=status, tg_id=tg_id, name=name)
    enroll.enroll()
    enroll.close()
    await state.clear()
    await bot.send_message(chat_id=ADMIN, text=f'✅ Новая запись\n'
                                               f'{get_datetime_str(year, month, day, time)}\n'
                                               f'{name}', reply_markup=keyboard_chat_with_user(tg_id))
