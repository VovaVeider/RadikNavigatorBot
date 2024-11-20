from datetime import datetime
from typing import List, Tuple

from bot.entity.shedule.DayShedule import DaySchedule
from bot.entity.shedule.TimeInterval import TimeInterval
from bot.entity.shedule.WeekShedule import WeekSchedule
from bot.repository.database import Database
from bot.entity.enum.WeekType import WeekType
from bot.entity.enum.DayOfWeek import DayOfWeek


class LessonRepository:
    def __init__(self, db: Database):
        self._db = db

    async def create_lesson(
            self, group_id: int, is_odd: WeekType, day: DayOfWeek, time_interval: TimeInterval, description: str
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
            is_odd.value,  # Используем .value для передачи числового значения
            day.value,  # Используем .value для передачи числового значения
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
                "is_odd": WeekType(record["is_odd"]),  # Преобразуем в тип WeekType
                "day": DayOfWeek(record["day"]),  # Преобразуем в тип DayOfWeek
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
            self, group_name: str, is_odd: WeekType, day: DayOfWeek
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
        records = await self._db.fetch(query, group_name, is_odd.value, day.value)  # Используем .value для значений
        lessons = [
            {
                "id": record["id"],
                "group_id": record["group_id"],
                "is_odd": WeekType(record["is_odd"]),  # Преобразуем в WeekType
                "day": DayOfWeek(record["day"]),  # Преобразуем в DayOfWeek
                "time_interval": TimeInterval(
                    start=record["time_start"], end=record["time_end"]
                ),
                "description": record["description"],
            }
            for record in records
        ]
        return lessons

    async def create_lessons(self, lessons: List[Tuple[int, WeekType, DayOfWeek, TimeInterval, str]]) -> None:
        """
        Creates multiple lessons in the schedule.
        Each lesson is represented as a tuple:
        (group_id, is_odd, day, time_interval, description)
        """
        query = """
            INSERT INTO schedule (group_id, is_odd, day, time_start, time_end, description)
            VALUES ($1, $2, $3, $4, $5, $6)
        """

        args = [
            (
                lesson[0],  # group_id
                lesson[1] == WeekType.ODD_WEEK,  # is_odd (convert to boolean)
                lesson[2].value,  # day (DayOfWeek)
                lesson[3].start,  # time_interval start
                lesson[3].end,  # time_interval end
                lesson[4]  # description
            )
            for lesson in lessons
        ]

        await self._db.executemany(query, args)

    async def get_schedule_by_day(self, group_id: int, week_type: WeekType, day: DayOfWeek) -> DaySchedule:
        """
        Fetches the schedule for a specific day and returns it as a DaySchedule object.
        """
        query = """
        SELECT time_start, time_end, description
        FROM schedule
        WHERE group_id = $1 AND is_odd = $2 AND day = $3
        ORDER BY time_start
        """
        records = await self._db.fetch(query, group_id, week_type == WeekType.ODD_WEEK, day.value)
        day_schedule = DaySchedule()
        for record in records:
            time_interval = TimeInterval(record["time_start"], record["time_end"])
            day_schedule.add_lesson(time_interval, record["description"])
        return day_schedule

    async def get_week_schedule(self, group_id: int) -> WeekSchedule:
        """
        Fetches the entire week's schedule for the given group.
        """
        # Determine the current week type (odd/even)
        week_type = WeekType.get_week_type(datetime(2024, 9, 2), datetime.now())  # Example; you can customize
        week_schedule = WeekSchedule()

        # Loop through all days of the week
        for day in DayOfWeek:
            # Get the schedule for the specific day
            day_schedule = await self.get_schedule_by_day(group_id, week_type, day)
            week_schedule.set_day_schedule(day, day_schedule)

        return week_schedule
