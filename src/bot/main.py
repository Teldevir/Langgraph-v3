import asyncio
from aiogram import Dispatcher, Bot

from src.core.data.db.chroma.utils import load_fixtures
from src.bot.bot import BotSingleton
from src.bot.handlers import router


def run() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    load_fixtures()
    bot: Bot = BotSingleton.get_instance()
    asyncio.run(dp.start_polling(bot))


if __name__ == '__main__':
    run()
