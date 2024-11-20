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

async def add_groups_if_not_exists(groups: List[str]) -> None:
    """
    Добавляет группы в таблицу, если таких групп еще нет.
    Сначала извлекает все существующие группы, чтобы избежать N+1 запросов.
    """
    # Извлекаем все группы из базы
    existing_groups = await database.fetch("SELECT name FROM groups WHERE name = ANY($1)", groups)
    existing_group_names = {group["name"] for group in existing_groups}

    # Фильтруем только те группы, которых нет в базе
    new_groups = [group for group in groups if group not in existing_group_names]

    if new_groups:
        # Вставляем новые группы
        query = "INSERT INTO groups (name) VALUES ($1)"
        await database.executemany(query, [(group,) for group in new_groups])