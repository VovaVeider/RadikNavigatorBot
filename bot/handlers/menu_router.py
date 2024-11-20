import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards import kb_cancel, ikb_start_add_group, ikb_groups_configure, kb_start_main_menu
from bot.utils.states.find_aud_state import FindAudState
from ..entity.enum.DayOfWeek import DayOfWeek
from ..entity.enum.WeekType import WeekType
from ..entity.shedule.UniversityShedule import UniversitySchedule
from ..parser.parser import Parser
from ..repository import group_repo as gr, user_repo as ur
from ..utils.others.shedule import shedule
from ..utils.states.upload_file_state import UploadFileState
from datetime import datetime

menu_router = Router()


@menu_router.message(F.text == "🔎 Найти аудиторию")
async def find_aud_handler(message: types.Message, state: FSMContext):
    await state.set_state(FindAudState.find_aud)
    await message.answer("Введи номер аудитории которую хочешь найти ( например: 155 )", reply_markup=kb_cancel())


@menu_router.message(F.text == "⚙️ Настройки")
async def find_aud_handler(message: types.Message, state: FSMContext):
    user = await ur.get_user(message.from_user.id)

    user_id = user.user_id
    group = await gr.get_group_by_id(user.group_id)
    group_name = "Отсутствует" if group is None else group["name"]
    role = "Администратор" if user.role == "admin" else "Пользователь"

    profile_text = f"<blockquote>👤 Профиль</blockquote>\n\n" \
                   f"<b>UID:</b> {user_id}\n" \
                   f"<b>Группа:</b> {group_name}\n" \
                   f"<b>Уровень доступа:</b> {role}"

    await message.answer(profile_text, reply_markup=ikb_start_add_group())


@menu_router.message(F.text == "🕒 Расписание на сегодня")
async def schedule_today_handler(message: types.Message, state: FSMContext):
    schedule_message = ""
    user = await ur.get_user(message.from_user.id)
    if (user is not None) and (user.group_id is not None):
        group = (await gr.get_group_by_id(user.group_id))["name"]
        print(shedule.get_all_groups())
        # TODO:вОЕНКА
        if group in shedule.get_all_groups():
            day = DayOfWeek.get_current_day()
            week_type = WeekType.get_week_type(datetime(2024, 9, 2), datetime.now())
            schedule_message += "<blockquote>📆 Расписание на сегодня </blockquote> " \
                                + "\n\n" + str(shedule.get_group_day_schedule(group, day, week_type))
        else:
            schedule_message += "⚠️ Расписание для вашей группы еще не добавлено. Обратитесь к админу."
    else:
        schedule_message += "⚠️ Необходимо установить группу для просмотра расписания"

    await message.answer(schedule_message)


@menu_router.message(F.text == "📆 Расписание на неделю")
async def schedule_today_handler(message: types.Message, state: FSMContext):
    schedule_message = ""
    print("aaaaaaaaaaaaaaaaaaa")
    user = await ur.get_user(message.from_user.id)
    if (user is not None) and (user.group_id is not None):
        group = (await gr.get_group_by_id(user.group_id))["name"]
        print(shedule.get_all_groups())
        if group in shedule.get_all_groups():
            day = DayOfWeek.get_current_day()
            week_type = WeekType.get_week_type(datetime(2024, 9, 2), datetime.now())
            for day in DayOfWeek:
                if day.value >= DayOfWeek.get_current_day().value:
                    schedule_string: str = str(shedule.get_group_day_schedule(group, day, week_type)).lstrip('\n')
                    print(schedule_string)
                    await message.answer(f"<blockquote>🗓 {day} </blockquote>"
                                         f" \n {schedule_string} \n\n")
        else:
            await message.answer("⚠️ Расписание для вашей группы еще не добавлено. Обратитесь к админу.")
    else:
        await message.answer("⚠️ Необходимо установить группу для просмотра расписания")


@menu_router.message(F.document)
async def upload_file_parser_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    user = await ur.get_user(message.from_user.id)
    document = message.document

    file_info = await message.bot.get_file(document.file_id)
    print(file_info)
    # Скачиваем файл
    file_path = "bot/bin/schedule.xlsx"
    await message.bot.download_file(file_info.file_path, file_path)
    await message.answer(f"✅ Файл успешно загружен и сохранен по пути {file_path}.")
    parse_message = True
    try:
        parser = Parser()
        grp_shedule: UniversitySchedule = parser.parse_file(file_path)
        shedule.merge_schedules(grp_shedule)
    except Exception as e:
        print(e)
        parse_message = False

    if parse_message:
        await message.answer("✅ Расписание успешно обновлено.", reply_markup=kb_start_main_menu(user))
        try:
            os.remove(file_path)  # Удаляем файл
        except Exception as e:
            await message.reply(f"Ошибка при удалении файла: {e}")
        return await state.clear()
    else:
        await state.clear()
        return await message.answer("⚠️ Произошла ошибка при обновлении расписания.", reply_markup=kb_start_main_menu(user))


@menu_router.message(F.text == "📂 Загрузка файла")
async def upload_file(message: types.Message, state: FSMContext):
    user = await ur.get_user(message.from_user.id)
    if user.role != "admin":
        return
    await message.answer("📂 Отправьте текстовый документ (.txt).", reply_markup=kb_cancel())
    await state.set_state(UploadFileState.upload_file)


@menu_router.message(F.text == "👥 Группы")
async def upload_file(message: types.Message):
    user = await ur.get_user(message.from_user.id)
    if user.role != "admin":
        return

    groups = await gr.get_groups()
    groups_message = "👥 Найденные группы:\n\n"

    if len(groups) != 0:
        couter_groups = 1
        for group in groups:
            id = group["id"]
            name = group["name"]

            groups_message += f"<blockquote><b>{couter_groups}. {name}</b> \n[gID: {id}]</blockquote>\n"
            couter_groups += 1

    else:
        return await message.answer("В базе данных не нашлось ни одной группы.")

    return await message.answer(groups_message, parse_mode='HTML', reply_markup=ikb_groups_configure())
