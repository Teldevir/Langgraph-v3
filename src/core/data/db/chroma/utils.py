from src.config import Settings, SettingsSingleton
from src.core.domain.document_service import DocumentService


def load_fixtures() -> None:
    settings: Settings = SettingsSingleton.get_instance()
    service = DocumentService()
    service.clear()
    path: str = settings.app.default_doc_file_path
    service.upload_from_file(path)
    print(f'[LOADED FILE]: {path}')