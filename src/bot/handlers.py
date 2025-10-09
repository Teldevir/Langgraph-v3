from typing import BinaryIO

from aiogram import types, Bot
from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import File

from src.bot.bot import BotSingleton
from src.core.domain.document_service import DocumentService
from src.core.domain.chat import ask

router = Router()

MAX_TELEGRAM_MESSAGE_LENGTH = 4096


def _split_message(text: str, limit: int = MAX_TELEGRAM_MESSAGE_LENGTH) -> list[str]:
    """Split text into telegram-safe chunks.

    The implementation prefers breaking on newlines or spaces, but always
    guarantees forward progress and hard-splits when no natural boundary is
    available.
    """

    if not text:
        return [""]

    chunks: list[str] = []
    length: int = len(text)
    start: int = 0

    while start < length:
        end: int = min(start + limit, length)

        if end < length:
            # Try to keep paragraphs intact by breaking on the nearest newline
            candidate: int = text.rfind("\n", start + 1, end)
            if candidate == -1:
                # Fall back to a whitespace boundary to avoid mid-word breaks
                candidate = text.rfind(" ", start + 1, end)

            if candidate != -1 and candidate >= start:
                end = candidate + 1

        if end <= start:
            # No suitable boundary found; enforce a hard split.
            end = min(start + limit, length)

        chunk = text[start:end]
        if not chunk:
            break

        chunks.append(chunk)
        start = end

    return chunks


async def _answer(message: types.Message, text: str) -> None:
    stringified: str = str(text)

    for chunk in _split_message(stringified):
        # Telegram counts characters slightly differently for some unicode
        # symbols, so we defensively enforce the hard limit at send time.
        if len(chunk) > MAX_TELEGRAM_MESSAGE_LENGTH:
            for index in range(0, len(chunk), MAX_TELEGRAM_MESSAGE_LENGTH):
                await message.answer(chunk[index:index + MAX_TELEGRAM_MESSAGE_LENGTH])
            continue

        await message.answer(chunk)


@router.message(F.text, Command('start'))
async def start(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /start')
    await _answer(message, "Привет! Отправь мне документ для загрузки или задай вопрос.")


@router.message(F.text, Command('chunks'))
async def get_chunks(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /chunks')
    document_service = DocumentService()
    chunks: list[str] = document_service.get_chunks()

    for chunk in chunks:
        await _answer(message, chunk)

@router.message(F.text, Command('search'))
async def search_document(message: types.Message):
    _, _, query = message.text.partition(' ')
    print(f'[BOT]: <{message.chat.id}> - /search {query}')
    document_service = DocumentService()
    context: str = document_service.search_with_formatting(query)

    await _answer(message, context)

@router.message(F.text)
async def question(message: types.Message):
    thread_id: int = message.chat.id
    print(f'[BOT]: <{thread_id}> - {message.text}')
    answer = ask(message.text, str(thread_id))

    await _answer(message, str(answer))


@router.message(F.document)
async def upload_document(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - file loaded')
    bot: Bot = BotSingleton.get_instance()
    doc_file: File = await bot.get_file(message.document.file_id)
    doc_file_bytes: BinaryIO | None = await bot.download_file(doc_file.file_path)
    content: str = doc_file_bytes.read().decode()
    document_service = DocumentService()
    document_service.upload_from_text(content)

    await _answer(message, 'Документ загружен!')