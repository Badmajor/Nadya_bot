import os

from environs import Env

env = Env()
env.read_env()

# Настройки Telegram
BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN = int(os.environ['ADMIN'])

# Индивидуальный настройки
ADMIN_NAME = {'i': 'Виктор', 'r': 'Виктора', 'd': 'Виктору', 'v': 'Виктора', 't': 'Виктором', 'p': 'Викторе'}
SESSION = 0.5  # Длительность сеанса в часах 0.1 = 6 минут
WORKING_MODE = (10, 19.5)  # Режим работы (С, ДО), допустимы float кратный SESSION
BREAK = (12, 14)  # Перерыв (С, ДО)
DAY_OFF = (6, 7)  # Выходные дни недели в виде числа, понедельник - 1, воскресенье - 7
DEFAULT_SESSIONS_FREE = False  # По умолчанию все сеансы свободны
HOLIDAYS = ((5, 1), (5, 9), (1, 1), (31, 1))  # праздники в формате (месяц, день)
AUTO_CONFIRM = False  # Автоматическое подтверждение


# ADMIN_NAME = {'i': 'Яна', 'r': 'Яны', 'd': 'Яне', 'v': 'Яны', 't': 'Яной', 'p': 'Яне'}