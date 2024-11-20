from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile

from bot.keyboards import kb_start_main_menu
from bot.utils.states.find_aud_state import FindAudState
from ..bin.auditories_config import auditoriums_to_zones
from ..repository import user_repo as ur
from ..utils.others.auditories_util import find_route
from ..utils.others.exists_auditory import exists_auditory
from ..utils.others.get_all_auditories import get_all_auditories

find_aud_router = Router()



@find_aud_router.message(StateFilter(FindAudState.current_aud))
async def current_aud_handler(message: types.Message, state: FSMContext):
    user = await ur.get_user(message.from_user.id)
    user_text = message.text.strip()

    if not exists_auditory(user_text, auditoriums_to_zones):
        await message.answer("😢 Такой аудитории не существует.", reply_markup=kb_start_main_menu(user))
        await state.clear()
        return

    state_data = await state.get_data()
    find_aud = state_data.get("find_aud")
    current_aud = user_text

    if current_aud == find_aud:
        await message.answer("🤷‍♂️ Вы уже находитесь в нужной аудитории.", reply_markup=kb_start_main_menu(user))
        await state.clear()
        return

    # Получение маршрута
    route = find_route(current_aud, find_aud)

    # Ответ пользователю
    if route:
        if find_aud == "209":
            await message.answer_photo(FSInputFile("bot/bin/images/2_209.png"), caption=route, reply_markup=kb_start_main_menu(user))
        else:
            await message.answer(route, reply_markup=kb_start_main_menu(user))
    else:
        await message.answer("Вы уже находитесь в нужной аудитории.", reply_markup=kb_start_main_menu(user))
    await state.clear()


@find_aud_router.message(StateFilter(FindAudState.find_aud))
async def find_aud_handler(message: types.Message, state: FSMContext):
    user = await ur.get_user(message.from_user.id)
    user_text = message.text.strip()

    if not exists_auditory(user_text, auditoriums_to_zones):
        await message.answer("😢 Такой аудитории не существует.", reply_markup=kb_start_main_menu(user))
        await state.clear()
        return


    await state.set_data(
        {
            "find_aud": user_text
        }
    )

    await message.answer("Введите аудиторию в которой находитесь в данный момент или расположенную рядом с вами.")
    await state.set_state(FindAudState.current_aud)


@find_aud_router.callback_query(lambda callback: callback.data.startswith("list_aud"))
async def list_aud_callback(callback: types.CallbackQuery):
    list_auditories = get_all_auditories(auditoriums_to_zones)
    if list_auditories:
        await callback.message.answer(list_auditories)
    else:
        await callback.message.answer("⚠️ Аудитории отсутствуют, обратитесь к администратору.")
    await callback.answer()

