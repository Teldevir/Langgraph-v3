from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from src.config import SettingsSingleton, Settings


settings: Settings = SettingsSingleton.get_instance()

db_host: str = settings.postgres.host
db_port: str = settings.postgres.port
db_name: str = settings.postgres.name
db_username: str = settings.postgres.username
db_password: str = settings.postgres.password


conn_string: str = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
conn_string_without_driver: str = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

engine: Engine = create_engine(conn_string)

Base: DeclarativeMeta = declarative_base()
Base.metadata.create_all(bind=engine)



