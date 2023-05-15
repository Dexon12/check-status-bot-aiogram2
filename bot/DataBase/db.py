import asyncpg


class DataBaseEngine:
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    async def get_pool(self) -> asyncpg.Pool:
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                user='postgres',
                password='password',
                database='postgres',
                port='5432',
                host='localhost'
            )
        return self._pool

    async def create_db(self):
        if self._pool is None:
            pool2 = await self.get_pool()
            print(pool2)
        print(self._pool)
        async with self._pool.acquire() as con:
            return await con.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT,
                    name VARCHAR(24),
                    surname VARCHAR(24),
                    nickname VARCHAR(24),
                    send_or_not BOOLEAN,
                    date TIMESTAMP
                )"""
            )

    @classmethod
    def get_engine(cls):
        return cls._instance

    async def select_something(self, user_id):
        async with self._pool.acquire() as con:
            return con.execute(
                """SELECT telegram_id FROM users WHERE telegram_id = $1""", user_id
            )


class UserService:

    @classmethod
    def get_engine(cls):
        return DataBaseEngine.get_engine()

    @classmethod
    async def insert_user(cls, user_id, name, surname, nickname, send_or_not, date):
        pool = await cls.get_engine().get_pool()
        async with pool.acquire() as con:
            await con.execute(
                """INSERT INTO users(telegram_id, name, surname, nickname, send_or_not, date) 
                VALUES ($1, $2, $3, $4, $5, $6)"""
                , user_id, name,
                surname, nickname, send_or_not, date
            )
