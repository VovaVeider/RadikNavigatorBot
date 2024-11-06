# Класс DaySchedule для работы с расписанием
from bot.parser.shedule.TimeInterval import TimeInterval


# Класс DaySchedule для работы с расписанием одного дня
class DaySchedule:
    def __init__(self):
        # Список для хранения интервалов времени и описания занятий
        self.schedule = []

    def add_lesson(self, time_interval: TimeInterval, description: str):
        """
        Добавление занятия в расписание. Принимает объект TimeInterval.
        """
        # Добавляем занятие в список
        self.schedule.append((time_interval, description))

        # Сортируем расписание по времени начала
        self.schedule.sort(key=lambda x: x[0].start)

    def __iter__(self):
        """
        Итератор, возвращающий занятия по порядку (в порядке времени начала).
        """
        for interval, description in self.schedule:
            yield interval, description

    def __str__(self):
        """
        Строковое представление расписания.
        """
        return "\n".join([f"{interval}: {description}" for interval, description in self.schedule])

    def has_lessons(self) -> bool:
        """
        Проверка, есть ли занятия в этот день.
        """
        return len(self.schedule) > 0
