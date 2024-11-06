from typing import Optional

from bot.config import database
from bot.utils.postgres.entity.User import User


async def add_user(user_id: int, group_id: int = None, role: str = "user"):
    query = "INSERT INTO users (user_id, group_id, role) VALUES ($1, $2, $3)"
    await database.execute(query, user_id, group_id, role)


async def get_user(user_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE user_id = $1"
    record = await database.fetchrow(query, user_id)

    if record:
        return User(
            id=record['id'],
            user_id=record['user_id'],
            group_id=record['group_id'],
            role=record['role']
        )

    return None


# Обновление группы юзера по его user_id
async def update_user_group(user_id: int, group_id: int):
    query = "UPDATE users SET group_id = $1 WHERE user_id = $2"
    await database.execute(query, group_id, user_id)