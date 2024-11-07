# Класс DaySchedule для работы с расписанием
from bot.entity.shedule.TimeInterval import TimeInterval


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
        Строковое представление расписания в формате:
        1. пр.Правовое регулирование инженерной деятельности
           проф.Гришко А.Я.   465 C
           ⏰ 08:10 - 09:45
        """
        formatted_schedule = []
        for i, (interval, description) in enumerate(self.schedule, start=1):
            # Форматируем строку для вывода с нумерацией, описанием и временем

            formatted_schedule.append(
                f"<b><i> {i}. {description}</i></b>\n"
                f"   ⏰ {interval.start.strftime('%H:%M')} - {interval.end.strftime('%H:%M')}"
            )

        return "<blockquote>📆 Расписание на сегодня </blockquote> "+"\n\n".join(formatted_schedule)

    def has_lessons(self) -> bool:
        """
        Проверка, есть ли занятия в этот день.
        """
        return len(self.schedule) > 0

#         schedule_message += \
#         """
# <blockquote>📆 Расписание на сегодня </blockquote>
#
# \t1. <b><i>пр.Правовое регулирование инженерной деятельности
# проф.Гришко А.Я.   465 C</i></b>
# ⏰ 08.10 - 09.45\n
# \t2. <b><i> л.Физическая культура и спорт
#    Спортзал C </i></b>
# ⏰ 09.55 - 11.30
#         """
#             # "1. Лекция по предмету ТИИ, преподаватель Орешков В.И., \n" \
#
#                            # "\t🚪 Аудитория: 128\n" \
#                            # "\t⏰ Время: 13:35 – 15:10\n\n" \
#                            # "2. Лабораторная по предмету ТИИ, преподаватель Орешков В.И.\n" \
#                            # "\t🚪 Аудитория: 128\n" \
#                            # "\t⏰ Время: 15:20 – 16:55