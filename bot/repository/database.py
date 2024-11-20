import asyncpg
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Подключение к базе данных"""
        self._pool = await asyncpg.create_pool(self._db_url)

    async def disconnect(self):
        """Закрытие подключения к базе данных"""
        await self._pool.close()

    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Выполняет запрос и возвращает все записи"""
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Выполняет запрос и возвращает одну запись"""
        async with self._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query: str, *args) -> str:
        """Выполняет запрос без возврата результата (например, INSERT, UPDATE)"""
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def executemany(self, query: str, args_list: list):
        async with self._pool.acquire() as conn:
            return await conn.executemany(query, args_list)


