import uvicorn
from fastapi import FastAPI

from src.core.data.db.chroma.utils import load_fixtures
from src.config import Settings, SettingsSingleton
from src.application.api import router


def run() -> None:
    app = FastAPI()
    app.include_router(router)
    load_fixtures()
    settings: Settings = SettingsSingleton.get_instance()
    uvicorn.run(app, host='0.0.0.0', port=settings.app.api_port)


if __name__ == '__main__':
    run()