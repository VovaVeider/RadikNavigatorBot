from typing import Optional, Dict, List

from bot.config import database


async def add_group(name: str):
    query = "INSERT INTO groups (name) VALUES ($1)"
    await database.execute(query, name)

# Найти группу по ID
async def get_group_by_id(group_id: int) -> Optional[Dict[str, any]]:
    query = "SELECT * FROM groups WHERE id = $1"
    return await database.fetchrow(query, group_id)

# Найти группу по имени
async def get_group_by_name(group_name: str) -> Optional[Dict[str, any]]:
    query = "SELECT * FROM groups WHERE name = $1"
    return await database.fetchrow(query, group_name)

# Добыть все имеющиеся группы
async def get_groups() -> List[Dict[str, any]]:
    query = "SELECT * FROM groups"
    return await database.fetch(query)

# Обновление имени группы по ID
async def update_group(group_id: int, new_name: str):
    query = "UPDATE groups SET name = $1 WHERE id = $2"
    await database.execute(query, new_name, group_id)


# Удаление группы по ID
async def delete_group(group_id: int):
    query = "DELETE FROM groups WHERE id = $1"
    await database.execute(query, group_id)