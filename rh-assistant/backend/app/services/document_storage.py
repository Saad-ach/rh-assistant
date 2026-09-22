from pathlib import Path

from app.core.config import settings


class DocumentStorage:
    def __init__(self) -> None:
        self.local_root = Path("storage") / "documents"

    def save(self, blob_name: str, content: bytes, content_type: str | None) -> str:
        if settings.DOCUMENT_STORAGE_MODE.lower() == "azure":
            if not settings.AZURE_STORAGE_CONNECTION_STRING or not settings.AZURE_STORAGE_CONTAINER:
                raise RuntimeError("Azure Blob Storage is not configured")
            from azure.core.exceptions import ResourceExistsError
            from azure.storage.blob import BlobServiceClient, ContentSettings

            client = BlobServiceClient.from_connection_string(
                settings.AZURE_STORAGE_CONNECTION_STRING
            )
            container = client.get_container_client(settings.AZURE_STORAGE_CONTAINER)
            try:
                container.create_container()
            except ResourceExistsError:
                pass
            container.upload_blob(
                name=blob_name,
                data=content,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type),
            )
            return f"azure://{settings.AZURE_STORAGE_CONTAINER}/{blob_name}"

        target = self.local_root / blob_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return str(target)


document_storage = DocumentStorage()
