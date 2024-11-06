from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from ..repository import user_repo as ur
from bot.keyboards import kb_start_main_menu

cancel_router = Router()



@cancel_router.message(F.text == "❌ Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    user = await ur.get_user(message.from_user.id)
    await message.answer("Действие отменено.", reply_markup=kb_start_main_menu(user))
