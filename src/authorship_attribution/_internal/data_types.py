from datetime import datetime
import os
import re
from typing import Optional

type AuthorId = int
type BookId = int


class DateRange:
    def __init__(self, start: datetime, end: datetime):
        self.start: datetime = start
        self.end: datetime = end

    def __iter__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            if isinstance(value, datetime):
                yield key, value.isoformat()
            else:
                yield key, value


class Author:
    def __init__(
        self,
        id: AuthorId,
        name: str,
        lifetime: Optional[DateRange],
        book_ids: list[BookId],
    ):
        self.id: AuthorId = id
        self.name: str = name
        self.lifetime: Optional[DateRange] = lifetime
        self.book_ids: list[BookId] = book_ids

    def __iter__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            if isinstance(value, DateRange):
                yield key, dict(value)
            else:
                yield key, value


class Book:
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

    def __iter__(self):
        for key in self.__dict__:
            value = getattr(self, key)
            if isinstance(value, datetime):
                yield key, value.isoformat()
            else:
                yield key, value

    def __get_string_file_content(self, file_name: str) -> Optional[str]:
        file_path = os.path.join(self.folder_path, file_name)
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r") as f:
            return f.read()

    def raw_content(self) -> Optional[str]:
        return self.__get_string_file_content("original.txt")

    @staticmethod
    def __normalise(text: str) -> str:
        subbed_text = re.sub(r"\s+", " ", text)
        return subbed_text.lower()

    def normalized_content(self) -> Optional[str]:
        raw_content = self.raw_content()
        if raw_content is None:
            return None
        return Book.__normalise(raw_content)
