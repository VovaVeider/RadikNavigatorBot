from aiogram.fsm.state import State, StatesGroup


class FindAudState(StatesGroup):
    find_aud = State()
    current_aud = State()