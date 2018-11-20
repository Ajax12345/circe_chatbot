import sqlite3, random, typing

class Users:
    avatar_colors = ['#3446FB', '#EA2323', '#C9C9C9', '#FFAB03', '#FFE003', '#03FF1E', '#14D229', '#14D2A1', '#D462FF', '#FE00C8', '#FE0060', '#00FEE3']
    class CirceUser:
        def __init__(self, _row:typing.List[str]) -> None:
            self.avatar_color, self.name = _row
        @property
        def initials(self):
            [_a, *_], [_b, *_] = self.name.split()
            return f'{_a}{_b}'
    @classmethod
    def add_user(cls, _name:str) -> typing.Callable:
        conn = sqlite3.connect('all_users.db')
        conn.execute("INSERT INTO users VALUES (?, ?)", [random.choice(cls.avatar_colors), _name])
        conn.commit()
        conn.close()
        return cls.all_users()
    @classmethod
    def all_users(cls) -> typing.Callable:
        return cls(list(sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")))
    def __init__(self, _rows:typing.List[typing.List[str]]) -> None:
        self._rows = _rows
    @property
    def num(self):
        return len(self._rows)
    def __iter__(self):
        for i in self._rows:
            yield self.__class__.CirceUser(i)
    def __len__(self):
        return len(self._rows)