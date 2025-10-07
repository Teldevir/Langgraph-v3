from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.config import Settings, SettingsSingleton


class QdrantSingleton:
    _instance: QdrantVectorStore | None = None
    _embeddings: OllamaEmbeddings | None = None

    @classmethod
    def _get_embeddings(cls, settings: Settings) -> OllamaEmbeddings:
        if cls._embeddings is None:
            cls._embeddings = OllamaEmbeddings(model=settings.langgraph.embedding_model)
        return cls._embeddings

    @classmethod
    def get_instance(cls) -> QdrantVectorStore:
        if cls._instance is None:
            settings: Settings = SettingsSingleton.get_instance()
            qdrant_client = QdrantClient(
                host=settings.qdrant.host,
                port=settings.qdrant.port,
                grpc_port=settings.qdrant.grpc_port,
                prefer_grpc=settings.qdrant.prefer_grpc,
            )

            cls._instance = QdrantVectorStore(
                client=qdrant_client,
                collection_name=settings.qdrant.collection_name,
                embeddings=cls._get_embeddings(settings),
            )
        return cls._instance
