from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.entity.User import User


def kb_start_main_menu(user: User = None):
    kb_menu = ReplyKeyboardBuilder()

    kb_menu.button(text="🔎 Найти аудиторию")


    if (user is not None) and (user.group_id is not None):
        kb_menu.button(text="🕒 Расписание на сегодня")
        kb_menu.button(text="📆 Расписание на неделю")

    if (user is not None) and (user.role == "admin"):
        kb_menu.button(text="📂 Загрузка файла")
        kb_menu.button(text="♻️ Конфигурация")
        kb_menu.button(text="👥 Группы")

    kb_menu.button(text="⚙️ Настройки")
    kb_menu.adjust(2)
    return kb_menu.as_markup(resize_keyboard=True)



def kb_cancel():
    kb_cancel = ReplyKeyboardBuilder()

    kb_cancel.button(text="❌ Отмена")
    kb_cancel.adjust(1)

    return kb_cancel.as_markup(resize_keyboard=True)
