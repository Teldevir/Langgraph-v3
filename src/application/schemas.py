from pydantic import BaseModel


class ChatMessageIn(BaseModel):
    message: str
    thread_id: str


class ChatMessageOut(BaseModel):
    answer: str