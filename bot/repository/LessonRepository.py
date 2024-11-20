from typing import List

from bot.entity.shedule.TimeInterval import TimeInterval
from bot.repository.database import Database


class LessonRepository:
    def __init__(self, db: Database):
        self._db = db

    async def create_lesson(
        self, group_id: int, is_odd: bool, day: str, time_interval: TimeInterval, description: str
    ) -> None:
        """
        Creates a new lesson in the schedule.
        """
        query = """
        INSERT INTO schedule (group_id, is_odd, day, time_start, time_end, description)
        VALUES ($1, $2, $3, $4, $5, $6)
        """
        await self._db.execute(
            query,
            group_id,
            is_odd,
            day,
            time_interval.start,
            time_interval.end,
            description,
        )

    async def get_lesson(
        self, lesson_id: int
    ) -> dict:
        """
        Fetches a lesson by its ID.
        Returns a dictionary with the lesson details or None if not found.
        """
        query = """
        SELECT id, group_id, is_odd, day, time_start, time_end, description
        FROM schedule
        WHERE id = $1
        """
        record = await self._db.fetchrow(query, lesson_id)
        if record:
            return {
                "id": record["id"],
                "group_id": record["group_id"],
                "is_odd": record["is_odd"],
                "day": record["day"],
                "time_interval": TimeInterval(
                    start=record["time_start"], end=record["time_end"]
                ),
                "description": record["description"],
            }
        return None

    async def update_lesson(
        self,
        lesson_id: int,
        time_interval: TimeInterval = None,
        description: str = None,
    ) -> None:
        """
        Updates the time interval and/or description of a lesson by its ID.
        """
        updates = []
        params = []

        if time_interval:
            updates.append("time_start = $1")
            updates.append("time_end = $2")
            params.extend([time_interval.start, time_interval.end])

        if description:
            updates.append("description = $3")
            params.append(description)

        params.append(lesson_id)
        query = f"""
        UPDATE schedule
        SET {', '.join(updates)}
        WHERE id = ${len(params)}
        """
        await self._db.execute(query, *params)

    async def delete_lesson(self, lesson_id: int) -> None:
        """
        Deletes a lesson by its ID.
        """
        query = "DELETE FROM schedule WHERE id = $1"
        await self._db.execute(query, lesson_id)

    async def delete_lessons_by_group_names(self, group_names: List[str]) -> None:
        """
        Deletes all lessons for the given list of group names using a single query with JOIN.
        """
        query = """
        DELETE FROM schedule
        USING groups
        WHERE schedule.group_id = groups.id
          AND groups.name = ANY($1)
        """
        await self._db.execute(query, group_names)

    async def get_lessons_by_group(
        self, group_name: str, is_odd: bool, day: str
    ) -> List[dict]:
        """
        Fetches all lessons for a given group name, for a specific week (odd or even), and for a specific day.
        Returns a list of lessons.
        """
        query = """
        SELECT schedule.id, schedule.group_id, schedule.is_odd, schedule.day, schedule.time_start, schedule.time_end, schedule.description
        FROM schedule
        JOIN groups ON schedule.group_id = groups.id
        WHERE groups.name = $1 AND schedule.is_odd = $2 AND schedule.day = $3
        ORDER BY schedule.time_start
        """
        records = await self._db.fetch(query, group_name, is_odd, day)
        lessons = [
            {
                "id": record["id"],
                "group_id": record["group_id"],
                "is_odd": record["is_odd"],
                "day": record["day"],
                "time_interval": TimeInterval(
                    start=record["time_start"], end=record["time_end"]
                ),
                "description": record["description"],
            }
            for record in records
        ]
        return lessons
