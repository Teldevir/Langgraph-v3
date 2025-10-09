from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models

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
                https=settings.qdrant.use_https,
                api_key=settings.qdrant.api_key,
            )

            embeddings = cls._get_embeddings(settings)
            cls._ensure_collection_exists(qdrant_client, settings, embeddings)

            cls._instance = QdrantVectorStore(
                client=qdrant_client,
                collection_name=settings.qdrant.collection_name,
                embedding=embeddings,
            )
        return cls._instance

    @classmethod
    def _ensure_collection_exists(
        cls,
        client: QdrantClient,
        settings: Settings,
        embeddings: OllamaEmbeddings,
    ) -> None:
        collection_name = settings.qdrant.collection_name
        if client.collection_exists(collection_name=collection_name):
            return

        vector_size = cls._get_vector_size(embeddings)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE,
            ),
        )

    @staticmethod
    def _get_vector_size(embeddings: OllamaEmbeddings) -> int:
        sample_embedding = embeddings.embed_query("vector size probe")
        if not sample_embedding:
            raise ValueError("Failed to determine embedding dimensionality")
        return len(sample_embedding)
