from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import SettingsSingleton
from src.core.data.db.chroma.config import ChromaSingleton

settings = SettingsSingleton.get_instance()


class DocumentService:
    def __init__(self):
        self.vector_store: Chroma = ChromaSingleton.get_instance()

    def search(self, query: str) -> list[Document]:
        try:
            return self.vector_store.similarity_search(
                query=query,
                k=settings.langgraph.similarity_search_k
            )
        except Exception as e:
            print(f'Ошибка при поиске: {e}')
            raise e

    def search_with_formatting(self, query: str) -> str:
        docs: list[Document] = self.search(query)
        return '\n'.join([doc.page_content for doc in docs])

    def upload_from_text(self, text: str) -> None:
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.langgraph.splitter_chunk_size,
                chunk_overlap=settings.langgraph.splitter_chunk_overlap,
                separators=settings.langgraph.separators,
                keep_separator=False,
                strip_whitespace=True,
            )
            splits: list[str] = text_splitter.split_text(text)
            self.vector_store.add_texts(splits)

        except Exception as e:
            print(f'Ошибка при загрузке: {e}')
            raise e

    def upload_from_file(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            content: str = '\n'.join(f.readlines())
            self.upload_from_text(content)

    def get_chunks(self) -> list[str]:
        data: dict[str, Any] = self.vector_store.get()
        chunks: list[str] = data.get('documents', [])
        return chunks

    def clear(self):
        ids = self.vector_store.get()['ids']
        if ids:
            self.vector_store.delete(ids)
