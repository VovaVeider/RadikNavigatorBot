from datetime import datetime
from enum import Enum


class WeekType(Enum):
    ODD_WEEK = 1
    EVEN_WEEK = 2

    @classmethod
    def get_week_type(cls, start_date: datetime, target_date: datetime = None) -> 'WeekType':
        """
        Определяет, является ли текущая неделя четной или нечетной, начиная с заданной начальной даты.
        Возвращает WeekType.ODD_WEEK или WeekType.EVEN_WEEK.
        """
        if target_date is None:
            target_date = datetime.now()

        # Разница в днях между целевой и начальной датами
        delta_days = (target_date - start_date).days

        # Номер недели с начальной даты (первая неделя имеет номер 1)
        week_number = delta_days // 7 + 1

        # Определение четности недели
        return WeekType.EVEN_WEEK if week_number % 2 == 0 else WeekType.ODD_WEEK
