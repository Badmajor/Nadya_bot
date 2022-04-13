import sqlite3

from data.loader import dt


class PostString:
    def __init__(self, w_year: int, w_month: int, w_day: int, w_time: float, status: int = None, tg_id: int = None,
                 phone: str = None, name: str = None):
        self.connect = sqlite3.connect(r'data/orders.db')
        self.cursor = self.connect.cursor()
        self.w_year = w_year
        self.w_month = w_month
        self.w_day = w_day
        self.w_time = w_time
        self.status = status
        self.tg_id = tg_id
        self.phone = phone
        self.name = name
        # w_time - время в формате флот 8:30 == 8.5
        # status - имеет 3 значения 0.занято 1.свободно -1.нерабочий
        # tg_id и следующие инфа о юзере
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS windows(
        w_year INT,
        w_month INT,
        w_day INT,
        w_time FLOAT, 
        status INT, 
        tg_id INT, 
        phone TEXT, 
        name TEXT);
        """)
        self.connect.commit()

    def make_win(self):
        data = (self.w_year, self.w_month, self.w_day, self.w_time, self.status, self.tg_id, self.phone, self.name)
        self.cursor.execute(
            """INSERT INTO windows(w_year, w_month, w_day, w_time, status, tg_id, phone, name)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", data)
        self.connect.commit()

    def enroll(self):
        data = (self.status, self.tg_id, self.phone, self.name, self.w_year, self.w_month, self.w_day, self.w_time)
        self.cursor.execute(
            """UPDATE windows SET status=?, tg_id=?, phone=?, name=? 
            WHERE w_year=? and w_month=? and w_day=? and w_time=?;""", data)
        self.connect.commit()

    def close(self):
        self.connect.close()


class GetData:
    """
    Обязательно закрывай после использования close(self) !!!!
    """

    def __init__(self, w_year: int = None, w_month: int = None, w_day: int = None, w_time: float = None,
                 status: int = None, tg_id: int = None, phone: str = None, name: str = None):
        self.connect = sqlite3.connect(r'data/orders.db')
        self.cursor = self.connect.cursor()
        self.w_year = w_year
        self.w_month = w_month
        self.w_day = w_day
        self.w_time = w_time
        self.status = status
        self.tg_id = tg_id
        self.phone = phone
        self.name = name

    def string(self):
        if self.w_year and self.w_month and self.w_day and self.w_time:
            self.cursor.execute("SELECT * FROM windows WHERE w_year=? and w_month=? and w_day=? and w_time=?;",
                                (self.w_year, self.w_month, self.w_day, self.w_time))
            return self.cursor.fetchone()
        if self.status:
            self.cursor.execute("SELECT * FROM windows WHERE status=?;", (self.status,))
            return self.cursor.fetchall()
        if self.tg_id:
            self.cursor.execute("SELECT * FROM windows WHERE tg_id=?;", (self.tg_id,))
            return self.cursor.fetchall()
        if self.phone:
            self.cursor.execute("SELECT * FROM windows WHERE phone=?;", (self.phone,))
            return self.cursor.fetchall()
        if self.name:
            self.cursor.execute("SELECT * FROM windows WHERE name=?;", (self.name,))
            return self.cursor.fetchall()

    def check_status(self) -> int:
        if self.w_year and self.w_month and self.w_day and self.w_time:
            self.cursor.execute("SELECT status FROM windows WHERE w_year=? and w_month=? and w_day=? and w_time=?;",
                                (self.w_year, self.w_month, self.w_day, self.w_time))
            try:
                return self.cursor.fetchone()[0]
            except TypeError:
                return -1
        else:
            return -1

    def check_month(self) -> bool:
        self.cursor.execute("SELECT * FROM windows WHERE w_month=?;",
                            (self.w_month,))
        for i in self.cursor.fetchall():
            if i[4] == 1:
                return True
        return False

    def check_day(self) -> bool:
        self.cursor.execute("SELECT * FROM windows WHERE w_month=? and w_day=?;",
                            (self.w_month, self.w_day))
        for i in self.cursor.fetchall():
            if i[4] == 1:
                return True
        return False

    def get_schedule_day(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM windows WHERE w_month=? and w_day=?;",
                            (self.w_month, self.w_day))
        return self.cursor.fetchall()

    def get_schedule_today(self) -> list[tuple]:
        self.cursor.execute("SELECT * FROM windows WHERE w_month=? and w_day=?;",
                            (dt.month, dt.day))
        list_sessions = self.cursor.fetchall()
        for i in list_sessions.copy():
            print(i)
            if i[3] < dt.hour-1 or i[4]:
                type(i[4])
                list_sessions.remove(i)
        return list_sessions

    def close(self):
        self.connect.close()


async def clear_old_data(month: int, day: int):
    """
    Удаляет записи предыдущих дней
    """
    connect = sqlite3.connect(r'data/orders.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM windows WHERE w_month<? and w_day<?;", (month, day))
    connect.commit()
