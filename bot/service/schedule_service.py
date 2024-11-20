import dataclasses
import logging
from datetime import datetime

from bot.config import database
from bot.entity.enum.DayOfWeek import DayOfWeek
from bot.entity.enum.WeekType import WeekType
from bot.entity.shedule.DayShedule import DaySchedule
from bot.entity.shedule.UniversityShedule import UniversitySchedule
from bot.entity.shedule.WeekShedule import WeekSchedule
from bot.repository.LessonRepository import LessonRepository
from bot.service.parser_service import ParserService
from bot.repository.group_repo import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclasses.dataclass
class UpdateScheduleReport:
    update_successful: bool
    groups: list[str]


class ScheduleService:
    def __init__(self, lesson_repository: LessonRepository, parser: ParserService):
        self.lesson_repository = lesson_repository
        self.parser = parser

    async def update_university_schedule_from_xlsx(self, xlsx_location: str) -> UpdateScheduleReport:
        try:
            return await self.update_university_schedule(self.parser.parse_file(xlsx_location))
        except Exception as e:
            logger.error(e)
            return UpdateScheduleReport(update_successful=False, groups=[])

    async def update_university_schedule(self, schedule: UniversitySchedule) -> UpdateScheduleReport:
        try:
            await self.lesson_repository.delete_lessons_by_group_names(schedule.get_all_groups())
            await add_groups_if_not_exists(schedule.get_all_groups())
            groups = {group_record['name']: group_record['id'] for group_record in (await get_groups())}

            lessons = [
                (groups[group_name], week_type, day, lesson[0], lesson[1])
                for day in DayOfWeek
                for week_type in WeekType
                for group_name in schedule
                for lesson in schedule.get_group_day_schedule(group_name, day, week_type)
            ]
            await self.lesson_repository.create_lessons(lessons)
            return UpdateScheduleReport(update_successful=True, groups=schedule.get_all_groups())
        except Exception as e:
            logger.error(e)
            return UpdateScheduleReport(update_successful=False, groups=[])

    async def get_week_schedule(self, group_id: int) -> WeekSchedule:
        return await self.lesson_repository.get_week_schedule(group_id)

    async def get_current_day_schedule(self, group_id: int) -> DaySchedule:
        week_type = WeekType.get_week_type(datetime(2024, 9, 2), datetime.now())
        day = DayOfWeek.get_current_day()
        return await self.lesson_repository.get_schedule_by_day(group_id, week_type, day)


schedule_service = ScheduleService(LessonRepository(database), ParserService())
