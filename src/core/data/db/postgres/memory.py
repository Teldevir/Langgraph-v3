from langgraph.checkpoint.postgres import PostgresSaver
from src.core.data.db.postgres.engine import conn_string_without_driver


def get_checkpointer():
    return PostgresSaver.from_conn_string(conn_string_without_driver)