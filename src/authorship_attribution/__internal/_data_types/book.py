from datetime import datetime
import os
from typing import Optional
from authorship_attribution.__internal._data_types import (
    BaseDataClass,
    AuthorId,
    BookId,
)


class Book(BaseDataClass):
    def __init__(
        self,
        id: BookId,
        title: str,
        language: str,
        author_ids: list[AuthorId],
        release_date: Optional[datetime],
        publication_date: Optional[datetime],
        content_length: int,
        folder_path: str,
    ):
        self.id: BookId = id
        self.title: str = title
        self.language: str = language
        self.author_ids: list[AuthorId] = author_ids
        self.release_date: Optional[datetime] = release_date
        self.publication_date: Optional[datetime] = publication_date
        self.content_length: int = content_length
        self.folder_path: str = folder_path

    def _content_path(self) -> str:
        return os.path.join(self.folder_path, "original.txt")

    def content(self) -> Optional[str]:
        if not self.has_content():
            return None
        with open(self._content_path(), "r") as f:
            return f.read()

    def has_content(self) -> bool:
        file_path = self._content_path()
        return os.path.exists(file_path)
