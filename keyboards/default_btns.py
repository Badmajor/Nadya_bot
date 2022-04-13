from aiogram.types import InlineKeyboardButton

from keyboards.callback_data import CancelCallback

back_btn = InlineKeyboardButton(text='<-Назад', callback_data=CancelCallback(home=False).pack())
cancel_btn = InlineKeyboardButton(text='Отмена', callback_data=CancelCallback(home=True).pack())
default_btns = (back_btn, cancel_btn)