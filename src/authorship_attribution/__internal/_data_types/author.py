from typing import Optional
from authorship_attribution.__internal._data_types import BaseDataClass, AuthorId, BookId, DateRange


class Author(BaseDataClass):
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
