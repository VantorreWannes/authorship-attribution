from datetime import datetime
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
        author_ids: list[AuthorId],
        release_date: Optional[datetime],
        publication_date: Optional[datetime],
        content_length: int,
        folder_path: str,
    ):
        self.id: BookId = id
        self.title: str = title
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