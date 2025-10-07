from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

from src.config import Settings, SettingsSingleton


class QdrantSingleton:
    _instance: Qdrant | None = None

    @classmethod
    def get_instance(cls) -> Qdrant:
        if cls._instance is None:
            settings: Settings = SettingsSingleton.get_instance()
            qdrant_client = QdrantClient(
                host=settings.qdrant.host,
                port=settings.qdrant.port,
                grpc_port=settings.qdrant.grpc_port,
            )

            cls._instance = Qdrant(
                client=qdrant_client,
                collection_name=settings.qdrant.collection_name,
                embeddings=OllamaEmbeddings(model=settings.langgraph.embedding_model),
                prefer_grpc=settings.qdrant.prefer_grpc,
            )
        return cls._instance
