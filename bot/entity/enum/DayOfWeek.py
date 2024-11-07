import re
from enum import Enum


class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def from_dirty_string(cls, dirty_string: str):
        """
        Парсит грязную строку и возвращает день недели из перечисления.
        Проверяет полное совпадение с названием дня недели, игнорируя пробелы и регистр.
        """
        # Приводим строку к нижнему регистру и убираем пробелы
        cleaned_string = dirty_string.strip().lower().replace(" ", "")

        # Словарь для ключевых подстрок, которые соответствуют каждому дню
        days_map = {
            'понедельник': cls.MONDAY,
            'пн': cls.MONDAY,
            'вторник': cls.TUESDAY,
            'вт': cls.TUESDAY,
            'среда': cls.WEDNESDAY,
            'срд': cls.WEDNESDAY,
            'четверг': cls.THURSDAY,
            'чт': cls.THURSDAY,
            'пятница': cls.FRIDAY,
            'пт': cls.FRIDAY,
            'суббота': cls.SATURDAY,
            'сб': cls.SATURDAY,
            'воскресенье': cls.SUNDAY,
            'вск': cls.SUNDAY,
        }

        # Перебираем все возможные ключевые строки
        for key, day in days_map.items():
            if cleaned_string == key:  # Проверка на точное совпадение
                return day

        # Если день не найден, выбрасываем ошибку
        raise ValueError(f"Не удалось распознать день недели: '{dirty_string}'")

    @classmethod
    def get_day_from_string(cls, dirty_string: str):
        """
        Этот метод будет возвращать день недели, если строка подходит под один из дней.
        Использует метод from_dirty_string, который парсит грязную строку и находит день.
        """
        try:
            day = cls.from_dirty_string(dirty_string)
            return day  # Возвращаем название дня недели
        except ValueError as e:
            return str(e)  # Возвращаем ошибку, если день не найден
