from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import SettingsSingleton
from src.core.data.db.qdrant.config import QdrantSingleton

settings = SettingsSingleton.get_instance()


class DocumentService:
    def __init__(self):
        self.vector_store: QdrantVectorStore = QdrantSingleton.get_instance()

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
        chunks: list[str] = []
        payload_key = getattr(self.vector_store, 'content_payload_key', 'page_content')
        offset = None

        while True:
            records, offset = self.vector_store.client.scroll(
                collection_name=settings.qdrant.collection_name,
                with_payload=True,
                with_vectors=False,
                limit=200,
                offset=offset,
            )

            if not records:
                break

            for record in records:
                if record.payload and payload_key in record.payload:
                    chunks.append(record.payload[payload_key])

            if offset is None:
                break

        return chunks

    def clear(self):
        offset = None

        while True:
            records, offset = self.vector_store.client.scroll(
                collection_name=settings.qdrant.collection_name,
                with_payload=False,
                with_vectors=False,
                limit=200,
                offset=offset,
            )

            if not records:
                break

            ids = [record.id for record in records if record.id is not None]
            if ids:
                self.vector_store.delete(ids=ids)

            if offset is None:
                break
