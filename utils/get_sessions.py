import math

from data.config import WORKING_MODE, SESSION
from data.loader import dt
from utils.converters import get_time_float


def get_session_btn(today: bool = False) -> list[str]:
    opn, cls = WORKING_MODE
    if today:
        minutes = math.ceil((dt.minute + 5) / (60 * SESSION)) * SESSION * 60
        opn = get_time_float(f'{dt.hour}:{int(minutes)}')
    sess = SESSION
    count = int((cls - opn) // sess)
    session_list = []
    for i in range(count):
        s_hour = str(int(opn))
        s_minutes = '00' if not opn % 1 else str(int(60 * (opn % 1)))
        session_list.append(f'{s_hour}:{s_minutes}')
        opn += sess
    session_list.append(f'{str(int(cls))}:{"00" if not cls % 1 else str(int(60 * (cls % 1)))}')
    return session_list
