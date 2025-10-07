from aiogram import Bot
from src.config import SettingsSingleton


class BotSingleton:
    _instance: Bot | None = None

    @classmethod
    def get_instance(cls) -> Bot:
        if cls._instance is None:
            settings = SettingsSingleton.get_instance()
            cls._instance = Bot(token=settings.app.bot_token)
        return cls._instance