from aiogram.fsm.state import State, StatesGroup


class UploadFileState(StatesGroup):
    upload_file = State()