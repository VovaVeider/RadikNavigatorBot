import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.bin.db import db
from bot.keyboards import kb_cancel, ikb_start_add_group, ikb_groups_configure, kb_start_main_menu
from bot.utils.states.find_aud_state import FindAudState
from ..utils.postgres.repository import user_repo as ur
from ..utils.postgres.repository import group_repo as gr
from ..utils.states.upload_file_state import UploadFileState

menu_router = Router()



@menu_router.message(F.text == "🔎 Найти аудиторию")
async def find_aud_handler(message: types.Message, state: FSMContext):
    await state.set_state(FindAudState.find_aud)

    await message.answer("Введи номер аудитории которую хочешь найти ( например: 155 )", reply_markup=kb_cancel())


@menu_router.message(F.text == "⚙️ Настройки")
async def find_aud_handler(message: types.Message, state: FSMContext):
    profile_text = "👤 Профиль студента\n\n" \
                   "В разработке -> 🛠"



    await message.answer(profile_text, reply_markup=ikb_start_add_group())


@menu_router.message(F.text == "➕ Расписание на сегодня")
async def schedule_today_handler(message: types.Message, state: FSMContext):
    schedule_message = ""
    user = await ur.get_user(message.from_user.id)
    if (user is not None) and (user.group_id is not None):
        schedule_message += "1. Лекция по предмету ТИИ, преподаватель Орешков В.И., \n" \
                           "\t🚪 Аудитория: 128\n" \
                           "\t⏰ Время: 13:35 – 15:10\n\n" \
                           "2. Лабораторная по предмету ТИИ, преподаватель Орешков В.И.\n" \
                           "\t🚪 Аудитория: 128\n" \
                           "\t⏰ Время: 15:20 – 16:55"
    else:
        schedule_message += "⚠️ Необходимо установить группу для просмотра расписания"

    await message.answer(schedule_message)


@menu_router.message(F.document)
async def upload_file_parser_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    user = await ur.get_user(message.from_user.id)
    document = message.document

    if document.mime_type == "text/plain":
        file_info = await message.bot.get_file(document.file_id)

        # Скачиваем файл
        file_path = "../bin/schedule.txt"
        await message.bot.download_file(file_info.file_path, file_path)
        await message.answer(f"✅ Файл успешно загружен и сохранен по пути {file_path}.")

        # parse_message = Парсинг(file_path, ......)
        # функцию с парсером создай в utils -> other или в bin, где удобно будет.

        # parse_message = True if parsing finished without errors
        # parse_message = False if parsing finished with some errors
        parse_message = True

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
    else:
        await message.reply("⚠️ Это не текстовый документ. Отправьте файл с расширением .txt.")

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


