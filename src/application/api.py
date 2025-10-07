from fastapi import APIRouter

from src.application.schemas import ChatMessageIn, ChatMessageOut
from src.core.domain.chat import ask

router = APIRouter()


@router.post('/chat')
async def chat(request: ChatMessageIn) -> ChatMessageOut:
    message: str = request.message
    thread_id: str = request.thread_id
    print(f'[API] <{thread_id}> - {message}>')
    answer: str = ask(message, thread_id)
    return ChatMessageOut(answer=answer)