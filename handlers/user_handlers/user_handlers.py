from contextlib import suppress

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from data.config import ADMIN_NAME, ADMIN
from data.loader import dp, bot
from keyboards.callback_data import SessionCallback, StartCallback
from keyboards.keyboards import keyboard_month, keyboard_enrolls_user, keyboard_start
from keyboards.keyboards_admin import keyboard_chat_with_user, keyboard_start_admin
from states.ChoiceTime import ChoiceTimeUser
from utils.check_data import check_enrolls_user
from utils.converters import get_datetime_str
from utils.database import PostString


@dp.message(commands=['start'], state='*')
async def command_start_handler(message: Message, state: FSMContext = None):
    tg_id = message.from_user.id if not message.from_user.is_bot else message.chat.id
    print(tg_id)
    with suppress(AttributeError):
        await state.clear()
    try:
        if tg_id == ADMIN:
            await message.edit_text(f'Чем могу помочь?',
                                    reply_markup=keyboard_start_admin())
        else:
            await message.edit_text(f'Чем могу помочь?\n',
                                    reply_markup=keyboard_start(tg_id))
    except TelegramBadRequest:
        if tg_id == ADMIN:
            msg = await message.answer(f'Приветики, {ADMIN_NAME.get("i")}😊\n'
                                       f'Начнем?)',
                                       reply_markup=keyboard_start_admin())
        else:
            msg = await message.answer(f'Приветики,😊\n'
                                       f'я интерактивный помошник {ADMIN_NAME.get("r")}.\n',
                                       reply_markup=keyboard_start(tg_id))
        await bot.delete_message(tg_id, msg.message_id - 1)


@dp.callback_query(StartCallback.filter(), state='*')
async def start_callback_handler(call: CallbackQuery, state: FSMContext, callback_data: StartCallback):
    tg_id = call.from_user.id
    btn = callback_data.action
    data = check_enrolls_user(tg_id)
    if btn == 'enroll':
        if data:
            await call.answer(f'Ближайшая запись\n'
                              f'{get_datetime_str(*data[0])}', show_alert=True)
        await state.set_state(ChoiceTimeUser.user_choice_month)
        await call.message.edit_text(f'Выбери месяц.',
                                     reply_markup=keyboard_month())
    if btn == 'cancel':
        if data:
            await call.message.edit_text(f'Твои записи,\nнажми на запись '
                                         f'если нужно отменить', reply_markup=keyboard_enrolls_user(data))
        else:
            await call.message.edit_text(f'Твоих записей нет', reply_markup=keyboard_start(tg_id))
    if btn == 'remind':
        if data:
            list_enrolls = [get_datetime_str(*i) for i in data]
            sep = '\n'
            with suppress(TelegramBadRequest):
                await call.message.edit_text(f'Твои записи:\n'
                                             f'{sep.join(list_enrolls)}',
                                             reply_markup=keyboard_start(tg_id))
        else:
            with suppress(TelegramBadRequest):
                await call.message.edit_text(f'Твоих записей нет.',
                                             reply_markup=keyboard_start(tg_id))
    await call.answer()


@dp.callback_query(SessionCallback.filter(), state='*')
async def cancel_enroll(call: CallbackQuery, callback_data: SessionCallback):
    user = call.from_user
    name, tg_id = user.full_name, user.id
    data = dict(callback_data).values()
    enroll_new = PostString(*data, status=1)
    enroll_new.enroll()
    enroll_new.close()
    await bot.send_message(chat_id=ADMIN, text=f'❌ Отмена записи\n '
                                               f'{get_datetime_str(*data)}\n'
                                               f'{name}', reply_markup=keyboard_chat_with_user(tg_id))
    await call.answer(f'❌ Отменила запись\n'
                      f'{get_datetime_str(*data)}\n'
                      f'{ADMIN_NAME.get("d")} написала.\n',
                      show_alert=True)
    await call.message.edit_text(f'❌ Отменила запись\n'
                                 f'{get_datetime_str(*data)}\n'
                                 f'{ADMIN_NAME.get("d")} написала.\n'
                                 f'Грустно теперь мне, раз мы не увидимся(((',
                                 reply_markup=keyboard_start(tg_id))
    await call.answer()
