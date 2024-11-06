from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from ..bin.db import db
from bot.keyboards import kb_start_main_menu, kb_cancel
from bot.utils.states.set_group_state import SetGroupState
from ..utils.postgres.repository import group_repo as gr
from ..utils.postgres.repository import user_repo as ur

set_group_router = Router()


@set_group_router.message(StateFilter(SetGroupState.set_group))
async def add_group_handler(message: types.Message, state: FSMContext):
    user_text = message.text.strip()

    group = await gr.get_group_by_name(user_text)

    if group is not None:
        await ur.update_user_group(message.from_user.id, group["id"])
        user = await ur.get_user(message.from_user.id)
        await message.answer("✅ Успех! Группа изменена.", reply_markup=kb_start_main_menu(user))
        await state.clear()
    else:
        await message.answer("❌ Такой группы не существует. Попробуйте ввести другую группу.")


@set_group_router.callback_query(lambda callback: callback.data.startswith("add_group"))
async def add_group_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await state.set_state(SetGroupState.set_group)
    await callback.message.answer("Введи номер своей группы:", reply_markup=kb_cancel())