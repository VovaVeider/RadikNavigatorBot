from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards import kb_cancel, kb_start_main_menu
from bot.repository import group_repo as gr, user_repo as ur
from bot.utils.states.configure_group_state import ConfigureGroupState

configure_groups_router = Router()


@configure_groups_router.message(StateFilter(ConfigureGroupState.add_group))
async def add_configure_group_handler(message: types.Message, state: FSMContext):
    new_name = message.text.strip()
    user = await ur.get_user(message.from_user.id)
    group = await gr.get_group_by_name(new_name)
    if group is None:
        await gr.add_group(new_name)
        await state.clear()
        return await message.answer("✅ Новая группа успешно добавлена в базу.", reply_markup=kb_start_main_menu(user))
    else:
        return await message.answer("⚠️ Группа с таким именем уже существует. Введите еще раз.")

@configure_groups_router.message(StateFilter(ConfigureGroupState.change_group))
async def change_configure_group_handler(message: types.Message, state: FSMContext):
    await message.answer("Бла бла бла еще в разработке, чуть позже с этим.")
    await state.clear()


@configure_groups_router.message(StateFilter(ConfigureGroupState.delete_group))
async def delete_configure_group_handler(message: types.Message, state: FSMContext):
    user_text = message.text.strip()
    user = await ur.get_user(message.from_user.id)
    try:
        user_text = int(user_text)
    except Exception as e:
        return await message.answer("❌ Некорректный gID группы. Введите еще раз.")

    group = await gr.get_group_by_id(user_text)
    if group is not None:
        await gr.delete_group(group["id"])
        await message.answer(f"✅ Группа с gID - {user_text} успешно удалена из базы.", reply_markup=kb_start_main_menu(user))
        return await state.clear()
    else:
        return await message.answer("❌ Группы с таким gID не найдено. Попробуйте еще раз.")


@configure_groups_router.callback_query(lambda callback: callback.data.startswith("configure_group_"))
async def configure_group_callback(callback: types.CallbackQuery, state: FSMContext):
    message_callback = callback.data[16:]

    if message_callback == "add":
        await state.set_state(ConfigureGroupState.add_group)
        await callback.message.answer("➕ Введите имя для создания новой группы. Например: 1415М", reply_markup=kb_cancel())
    elif message_callback == "change":
        await state.set_state(ConfigureGroupState.change_group)
        await callback.message.answer("✏️ Введите новое имя группы.", reply_markup=kb_cancel())
    elif message_callback == "delete":
        await state.set_state(ConfigureGroupState.delete_group)
        await callback.message.answer("🗑 Введите gID группы, которую хотите удалить.", reply_markup=kb_cancel())

    return await callback.answer()