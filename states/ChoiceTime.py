from aiogram.dispatcher.filters.state import StatesGroup, State


class ChoiceTimeUser(StatesGroup):
    user_choice_month = State()
    user_choice_date = State()
    user_choice_time = State()


class ChoiceTimeAdmin(StatesGroup):
    admin_choice_month = State()
    admin_choice_date = State()
    admin_choice_time = State()
    admin_post_data_db = State()
