
from datetime import time
from typing import Dict

from bot.entity.enum.DayOfWeek import DayOfWeek
from bot.entity.shedule.DayShedule import DaySchedule
from bot.entity.shedule.TimeInterval import TimeInterval


# Класс WeekSchedule для работы с расписанием на всю неделю
class WeekSchedule:
    def __init__(self):
        # Словарь для хранения расписания для каждого дня недели
        self.week_schedule: Dict[DayOfWeek, DaySchedule] = {
            DayOfWeek.MONDAY: DaySchedule(),
            DayOfWeek.TUESDAY: DaySchedule(),
            DayOfWeek.WEDNESDAY: DaySchedule(),
            DayOfWeek.THURSDAY: DaySchedule(),
            DayOfWeek.FRIDAY: DaySchedule(),
            DayOfWeek.SATURDAY: DaySchedule(),
            DayOfWeek.SUNDAY: DaySchedule()
        }

    def add_lesson(self, day: DayOfWeek, time_interval: TimeInterval, description: str):
        """
        Добавление занятия в расписание для конкретного дня недели.
        """
        self.week_schedule[day].add_lesson(time_interval, description)

    def set_day_schedule(self, day: DayOfWeek, day_schedule: DaySchedule):
        """
        Устанавливает расписание для конкретного дня недели.
        """
        self.week_schedule[day] = day_schedule

    def get_day_schedule(self, day: DayOfWeek) -> str:
        """
        Получение расписания для конкретного дня недели.
        Возвращает строку с расписанием, если есть занятия, или сообщение, если занятий нет.
        """
        day_schedule = self.week_schedule[day]
        if day_schedule.has_lessons():
            return f"{day.name}:\n{str(day_schedule)}"
        else:
            return f"{day.name}:\nNo lessons today."

    def __str__(self):
        """
        Строковое представление расписания на всю неделю.
        """
        week_str = []
        for day in DayOfWeek:
            week_str.append(f"{day.name}:")
            week_str.append(str(self.week_schedule[day]))
            week_str.append("")  # пустая строка для разделения дней
        return "\n".join(week_str)


if __name__ == "__main__":
    week_schedule = WeekSchedule()

    # Создаем объекты TimeInterval для разных дней
    math_time = TimeInterval(time(9, 0), time(10, 30))
    physics_time = TimeInterval(time(13, 0), time(14, 30))
    history_time = TimeInterval(time(10, 45), time(12, 0))

    # Добавляем занятия для разных дней недели
    week_schedule.add_lesson(DayOfWeek.MONDAY, math_time, "Math Lecture")
    week_schedule.add_lesson(DayOfWeek.MONDAY, physics_time, "Physics Lab")
    week_schedule.add_lesson(DayOfWeek.WEDNESDAY, history_time, "History Seminar")

    # Создаем новое расписание для четверга
    thursday_schedule = DaySchedule()
    thursday_schedule.add_lesson(TimeInterval(time(9, 0), time(10, 30)), "Thursday Math")
    thursday_schedule.add_lesson(TimeInterval(time(11, 0), time(12, 30)), "Thursday English")

    # Устанавливаем расписание для четверга
    week_schedule.set_day_schedule(DayOfWeek.THURSDAY, thursday_schedule)

    # Вывод расписания на всю неделю
    print(week_schedule)