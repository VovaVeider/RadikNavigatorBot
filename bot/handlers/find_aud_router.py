from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards import kb_start_main_menu
from bot.utils.states.find_aud_state import FindAudState
from ..utils.postgres.repository import user_repo as ur


find_aud_router = Router()


@find_aud_router.message(StateFilter(FindAudState.find_aud))
async def find_aud_handler(message: types.Message, state: FSMContext):
    # todo Проверки
    user = await ur.get_user(message.from_user.id)
    user_text = message.text.strip()
    stage_of_aud = None
    try:
        stage_of_aud = int(user_text[0])
    except Exception as e:
        print(e)
        await state.clear()
        await message.answer("❌ Неверный номер аудитории", reply_markup=kb_start_main_menu(user))
        return

    not_find_aud_text = "Аудитория не найдена 😢"
    result_answer = ""

    if user_text == "155":
        result_answer += f"🧭 Месторасположение:\n\n" \
                             f"Этаж: {stage_of_aud}\n" \
                             f"Левое крыло -> Кафедра САПР ВС\n"
    else:
        result_answer = f'Аудитория находится на {stage_of_aud} этаже.' if 1 <= stage_of_aud <= 4 else not_find_aud_text

    await message.answer(result_answer, reply_markup=kb_start_main_menu(user))
    await state.clear()


