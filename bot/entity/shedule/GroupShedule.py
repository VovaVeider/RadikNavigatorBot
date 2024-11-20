from bot.entity.enum.DayOfWeek import DayOfWeek
from bot.entity.enum.WeekType import WeekType
from bot.entity.shedule import WeekShedule, DayShedule
from bot.entity.shedule.TimeInterval import TimeInterval
from bot.entity.shedule.WeekShedule import WeekSchedule


class GroupSchedule:
    def __init__(self):
        self.schedule = {
            WeekType.ODD_WEEK: WeekSchedule(),  # Расписание для нечетной недели
            WeekType.EVEN_WEEK: WeekSchedule()  # Расписание для четной недели
        }

    def add_lesson(self, weekday_type: WeekType, day: DayOfWeek, time_interval: TimeInterval, description: str):
        """
        Добавление занятия для определенной недели (четная или нечетная).
        """
        self.schedule[weekday_type].add_lesson(day, time_interval, description)

    def set_week_schedule(self, weekday_type: WeekType, week_schedule: WeekShedule):
        """
        Добавление занятия для определенной недели (четная или нечетная).
        """
        self.schedule[weekday_type] = week_schedule

    def get_day_schedule(self, day: DayOfWeek, weekday_type: WeekType) -> DayShedule:
        """
        Получение расписания для конкретного дня недели и типа недели (четная или нечетная).
        """
        return self.schedule[weekday_type].get_day_schedule(day)

    def __str__(self):
        """
        Строковое представление расписания для группы на обе недели (четную и нечетную).
        """
        return f"Odd Week Schedule:\n{self.schedule[WeekType.ODD_WEEK]}\n\nEven Week Schedule:\n{self.schedule[WeekType.EVEN_WEEK]}"

