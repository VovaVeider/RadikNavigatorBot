from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_start_add_group():
    ikb_start_add_group = InlineKeyboardBuilder()
    ikb_start_add_group.button(text="➕ Установить группу", callback_data="add_group")


    return ikb_start_add_group.as_markup()


def ikb_groups_configure():
    ikb_groups_configure = InlineKeyboardBuilder()
    ikb_groups_configure.button(text="➕ Добавить", callback_data="configure_group_add")
    ikb_groups_configure.button(text="✏️ Редактировать", callback_data="configure_group_change")
    ikb_groups_configure.button(text="🗑 Удалить", callback_data="configure_group_delete")

    ikb_groups_configure.adjust(2)
    return ikb_groups_configure.as_markup()
