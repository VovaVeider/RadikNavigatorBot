from aiogram import types
from aiogram import Router


from ..keyboards import kb_start_main_menu, ikb_start_add_group

from aiogram.filters.command import Command

from ..repository import user_repo as ur

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user = await ur.get_user(user_id)
    await message.answer("Привет, я бот помощник студенту радика.", reply_markup=kb_start_main_menu(user))

    if user is None:
        await ur.add_user(user_id)
        return await message.answer("Я не нашел тебя в своей базе данных, выбери пожалуйста группу",
                             reply_markup=ikb_start_add_group())
    await message.answer("Выбери нужное действие")





