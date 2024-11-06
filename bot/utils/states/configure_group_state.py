from aiogram.fsm.state import State, StatesGroup


class ConfigureGroupState(StatesGroup):
    add_group = State()
    change_group = State()
    delete_group = State()