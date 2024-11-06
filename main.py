import asyncio

from bot.config import dp, bot, database
from bot.handlers.admin.configure_groups_router import configure_groups_router
from bot.handlers.find_aud_router import find_aud_router
from bot.handlers.menu_router import menu_router
from bot.handlers.cancel_router import cancel_router
from bot.handlers.set_group_router import set_group_router
from bot.handlers.start import start_router



def includes_routers():

    dp.include_router(cancel_router) # Всегда вверху

    dp.include_router(configure_groups_router)
    dp.include_router(start_router)
    dp.include_router(set_group_router)
    dp.include_router(find_aud_router)
    dp.include_router(menu_router)


async def start_bot():
    await database.connect()
    print("База данных подключена")


async def stop_bot():
    await database.disconnect()
    print("База данных отключена")


async def main() -> None:
    includes_routers()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == '__main__':
    asyncio.run(main())

