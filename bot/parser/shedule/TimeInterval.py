import re
from datetime import datetime, time


class TimeInterval:
    def __init__(self, start: time, end: time):
        """
        Инициализация интервала времени, используя объекты time для начала и конца.
        """
        if start >= end:
            raise ValueError("Время начала должно быть раньше времени окончания")
        self.start = start
        self.end = end

    def __str__(self):
        """
        Возвращает строковое представление интервала времени в формате 'HH:MM - HH:MM'.
        """
        return f"{self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')}"

    @classmethod
    def from_string(cls, interval_string):
        """
        Создание объекта TimeInterval из строки в формате 'HH:MM - HH:MM'.
        """
        try:
            start_str, end_str = interval_string.split(" - ")
            start = datetime.strptime(start_str, '%H:%M').time()
            end = datetime.strptime(end_str, '%H:%M').time()
            return cls(start=start, end=end)
        except ValueError:
            raise ValueError("Формат строки должен быть 'HH:MM - HH:MM'")

    @classmethod
    def from_dirty_string(cls, dirty_string):
        """
        Парсинг строк с различными форматами и игнорированием пробелов:
        '09.30-10.30', '9:30-10:30', '8.30 12.40', с пробелами в любом месте.
        """
        # Удаляем все пробелы из входной строки
        cleaned_string = dirty_string.replace(" ", "").replace('\n','')

        # Поддерживаем форматы вида 'HH.MM-HH.MM', 'HH:MM-HH:MM'
        pattern = r'(\d{1,2})[:\.](\d{2})[-](\d{1,2})[:\.](\d{2})'

        match = re.match(pattern, cleaned_string)
        if not match:
            raise ValueError("Строка не соответствует ожидаемому формату времени")

        # Парсим часы и минуты из строки
        start_hour, start_minute, end_hour, end_minute = map(int, match.groups())

        # Создаём объекты time для начала и конца интервала
        start = time(start_hour, start_minute)
        end = time(end_hour, end_minute)

        # Проверка на корректность интервала
        if start >= end:
            raise ValueError("Время начала должно быть раньше времени окончания")

        return cls(start=start, end=end)

    def to_string(self):
        """
        Метод для сохранения интервала времени в строку.
        """
        return str(self)


print(TimeInterval.from_dirty_string('13:35 - 15.10'))
