from bot.entity.enum.DayOfWeek import DayOfWeek
from bot.entity.shedule.DayShedule import DaySchedule
from bot.entity.shedule.WeekShedule import WeekSchedule


def week_schedule_to_string(week_schedule: WeekSchedule, start_day: DayOfWeek):
    result = 'Расписание на неделю:'
    for day in DayOfWeek:
        if day.value < start_day.value:
            continue
        result += week_schedule.get_day_schedule(day)



