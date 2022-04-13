from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.loader import dp
from handlers.user_handlers.user_handlers import command_start_handler
from keyboards.callback_data import CancelCallback


@dp.callback_query(CancelCallback.filter(), state='*')
async def cancel_btn_handler(call: CallbackQuery, state: FSMContext, callback_data: CancelCallback):
    await state.clear()
    await call.answer()
    await command_start_handler(call.message)
