import asyncpg
import aiofiles

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
                password='Dexon',
                database='postgres',
                port='5432',
                host='localhost'
            )
        return self._pool

    async def create_db(self) -> None: # CHECK THIS CODE
        """Creates database scheme if there does not exist a table named `users`"""

        pool = await self.get_pool()
        is_table = await self.check_table_exists(pool, 'users')
        if not is_table:
            async with aiofiles.open('bot/services/init_records.sql', mode='r') as fd:
                raw_query = await fd.read()

            async with pool.acquire() as conn:
                await conn.execute(raw_query)


    async def check_table_exists(self, pool, table_name): # CHECK THIS CODE
        async with pool.acquire() as connection:
            result = await connection.fetchval('''
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE  table_schema = 'public'
                    AND    table_name   = $1
                );
            ''', table_name)
        return result


    @property
    def pool(self) -> asyncpg.Pool:
        return self._pool


    @classmethod
    def get_engine(cls):
        return cls._instance


class UserService:

    @classmethod
    def get_engine(cls):
        return DataBaseEngine.get_engine()

    @classmethod
    async def insert_user(cls, user_id, name, surname, nickname, is_subscribed, date):
        pool = await cls.get_engine().get_pool()
        async with pool.acquire() as con:
            await con.execute(
                """INSERT INTO users(telegram_id, name, surname, nickname, is_subscribed , date) 
                VALUES ($1, $2, $3, $4, $5, $6)"""
                , user_id, name,
                surname, nickname, is_subscribed, date
            )

    @classmethod
    async def delete_all(cls, user_id):
        pool = cls.get_engine().pool
        
        async with pool.acquire() as con:
            return await con.execute(
                """DELETE FROM users WHERE telegram_id = $1""", user_id
            )

    # @classmethod
    # async def select_something(cls, user_id):
    #     pool = cls.get_engine().pool
    #
    #     async with pool.acquire() as con:
    #         return await con.execute(
    #            """SELECT telegram_id FROM users WHERE telegram_id = $1""", user_id
    #        )

    @classmethod
    async def take_subscribe(cls, tg_id):
        pool = cls.get_engine().pool

        async with pool.acquire() as con:
            result = await con.fetch(
                """SELECT is_subscribed FROM users WHERE telegram_id = $1""", tg_id
            )
            return [row[0] for row in result]
    @classmethod
    async def update_subscribe(cls, tg_id):
        pool = cls.get_engine().pool

        async with pool.acquire() as con:
            return await con.execute(
                """UPDATE users SET subscribe = False WHERE telegram_id = $1""", tg_id
            )

    @classmethod
    async def select_name(cls, tg_id):
        pool = cls.get_engine().pool

        async with pool.acquire() as con:
            result = await con.fetch(
                """SELECT name, surname FROM users WHERE telegram_id = $1""", tg_id
            )
            return [row[0] for row in result]
    
    @classmethod
    async def select_users_id(cls):
        pool = cls.get_engine().pool

        async with pool.acquire() as con:
            result = await con.fetch(
                """SELECT telegram_id FROM users"""
            )
            return [row[0] for row in result]
 