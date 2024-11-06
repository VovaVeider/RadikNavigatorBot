from datetime import time

from bot.entity.enum.DayOfWeek import DayOfWeek
from bot.entity.enum.WeekType import WeekdayType
from bot.entity.shedule.GroupShedule import GroupSchedule

from typing import Dict, Iterator

from bot.entity.shedule.TimeInterval import TimeInterval


class UniversitySchedule:
    def __init__(self):
        self.groups_schedule: Dict[str, GroupSchedule] = {}

    def add_group(self, group_name: str):
        """
        Добавление группы в расписание университета.
        """
        if group_name not in self.groups_schedule:
            self.groups_schedule[group_name] = GroupSchedule()

    def get_group_schedule(self, group_name: str, weekday_type: WeekdayType) -> str:
        """
        Получение расписания группы для четной или нечетной недели.
        """
        group_schedule = self.groups_schedule.get(group_name)
        if group_schedule:
            return str(group_schedule.schedule[weekday_type])
        else:
            return f"Group {group_name} not found."

    def get_group_day_schedule(self, group_name: str, day: DayOfWeek, weekday_type: WeekdayType) -> str:
        """
        Получение расписания группы на конкретный день недели (четная или нечетная неделя).
        """
        group_schedule = self.groups_schedule.get(group_name)
        if group_schedule:
            return group_schedule.get_day_schedule(day, weekday_type)
        else:
            return f"Group {group_name} not found."

    def merge_schedules(self, other: 'UniversitySchedule'):
        """
        Объединение расписаний: добавляет все расписания групп из другого объекта UniversitySchedule,
        кроме тех групп, которые уже существуют в текущем расписании.
        """
        for group_name, group_schedule in other.groups_schedule.items():
            if group_name not in self.groups_schedule:
                self.groups_schedule[group_name] = group_schedule

    def __iter__(self) -> Iterator[str]:
        """
        Итератор для перебора всех групп в расписании университета.
        Возвращает имена групп.
        """
        return iter(self.groups_schedule.keys())

    def __str__(self):
        """
        Строковое представление расписания для всех групп в университете.
        """
        result = "University Schedule:\n"
        for group_name, group_schedule in self.groups_schedule.items():
            result += f"\nGroup: {group_name}\n{group_schedule}\n"
        return result
if __name__ == "__main__":
    # Создаем два университета с расписаниями для групп
    university_schedule_1 = UniversitySchedule()
    university_schedule_2 = UniversitySchedule()

    # Добавляем группы и занятия в первый университет
    university_schedule_1.add_group("Group A")
    university_schedule_1.add_group("Group B")

    math_time = TimeInterval(time(9, 0), time(10, 30))
    physics_time = TimeInterval(time(13, 0), time(14, 30))

    university_schedule_1.groups_schedule["Group A"].add_lesson(WeekdayType.ODD_WEEK,DayOfWeek.MONDAY, math_time, "Math Lecture", )
    university_schedule_1.groups_schedule["Group B"].add_lesson(WeekdayType.EVEN_WEEK,DayOfWeek.TUESDAY, physics_time, "Physics Lab")

    # Добавляем группы и занятия во второй университет
    university_schedule_2.add_group("Group C")
    university_schedule_2.add_group("Group B")  # Группа "Group B" уже есть в первом университете, её не добавим при объединении

    history_time = TimeInterval(time(10, 0), time(11, 30))
    university_schedule_2.groups_schedule["Group C"].add_lesson(WeekdayType.EVEN_WEEK,DayOfWeek.WEDNESDAY, history_time, "History Lecture")
    university_schedule_2.groups_schedule["Group B"].add_lesson(WeekdayType.ODD_WEEK,DayOfWeek.THURSDAY, physics_time, "Physics Lab")

    # Объединяем расписания двух университетов
    university_schedule_1.merge_schedules(university_schedule_2)

    # Печатаем итоговое расписание
    print(university_schedule_1)

    # Используем итератор для перебора групп в расписании
    for group in university_schedule_1:
        print(f"Group: {group}")
