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


@router.message(F.text, Command('start'))
async def start(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /start')
    await message.answer("Привет! Отправь мне документ для загрузки или задай вопрос.")


@router.message(F.text, Command('chunks'))
async def get_chunks(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /chunks')
    document_service = DocumentService()
    chunks: list[str] = document_service.get_chunks()

    for chunk in chunks:
        await message.answer(chunk)

@router.message(F.text, Command('search'))
async def search_document(message: types.Message):
    _, _, query = message.text.partition(' ')
    print(f'[BOT]: <{message.chat.id}> - /search {query}')
    document_service = DocumentService()
    context: str = document_service.search_with_formatting(query)

    await message.answer(context)

@router.message(F.text)
async def question(message: types.Message):
    thread_id: int = message.chat.id
    print(f'[BOT]: <{thread_id}> - {message.text}')
    answer = ask(message.text, str(thread_id))

    await message.answer(str(answer))


@router.message(F.document)
async def upload_document(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - file loaded')
    bot: Bot = BotSingleton.get_instance()
    doc_file: File = await bot.get_file(message.document.file_id)
    doc_file_bytes: BinaryIO | None = await bot.download_file(doc_file.file_path)
    content: str = doc_file_bytes.read().decode()
    document_service = DocumentService()
    document_service.upload_from_text(content)

    await message.answer('Документ загружен!')