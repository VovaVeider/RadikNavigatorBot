from .database import Database
from ..entity.shedule.DayShedule import DaySchedule
from ..entity.shedule.TimeInterval import TimeInterval


class DayScheduleRepository:
    def __init__(self, db: Database):
        self._db = db

    async def create_schedule_for_day(self, group_id: int, is_odd: bool, day: str, day_schedule: DaySchedule) -> None:
        """
        Creates a schedule for an entire day using a DaySchedule object.

        Parameters:
        - group_id (int): The group ID the schedule belongs to.
        - is_odd (bool): Whether the schedule applies to odd weeks.
        - day (str): The day of the schedule (e.g., "Monday").
        - day_schedule (DaySchedule): An object containing the day's schedule.
        """
        query = """
        INSERT INTO schedule (group_id, is_odd, day, time_start, time_end, description)
        VALUES ($1, $2, $3, $4, $5, $6)
        """
        # Extract lessons from the DaySchedule object
        values = [
            [
                group_id,
                is_odd,
                day,
                lesson[0].start,  # TimeInterval.start
                lesson[0].end,  # TimeInterval.end
                lesson[1],  # Description
            ]
            for lesson in day_schedule.schedule
        ]
        await self._db.execute_many(query, values)

    async def get_schedule_by_day(self, group_id: int, is_odd: bool, day: str) -> DaySchedule:
        """
        Fetches the schedule for a specific day and returns it as a DaySchedule object.
        """
        query = """
        SELECT time_start, time_end, description
        FROM schedule
        WHERE group_id = $1 AND is_odd = $2 AND day = $3
        ORDER BY time_start
        """
        records = await self._db.fetch(query, group_id, is_odd, day)
        day_schedule = DaySchedule()
        for record in records:
            time_interval = TimeInterval(record["time_start"], record["time_end"])
            day_schedule.add_lesson(time_interval, record["description"])
        return day_schedule


