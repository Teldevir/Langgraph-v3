from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config import SettingsSingleton, Settings


class ChromaSingleton:
    _instance: Chroma | None = None

    @classmethod
    def get_instance(cls) -> Chroma:
        if cls._instance is None:
            settings: Settings = SettingsSingleton.get_instance()
            chroma_client = HttpClient(
                host=settings.chroma.host,
                port=settings.chroma.port,
            )

            cls._instance = Chroma(
                embedding_function=OllamaEmbeddings(model=settings.langgraph.embedding_model),
                client=chroma_client,
            )
        return cls._instance

