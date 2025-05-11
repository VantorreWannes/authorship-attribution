from typing import Optional
from authorship_attribution.__internal._data_types.base_type import BaseDataClass
from authorship_attribution.__internal._data_types.date_range import DateRange
from authorship_attribution.__internal._data_types.type_aliases import AuthorId, BookId


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
