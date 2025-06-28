from datetime import date
from authorship_attribution._internals.types.aliases import AuthorId, Id


class Book:
    def __init__(
        self,
        id: Id,
        title: str,
        issued: date,
        authors: list[AuthorId],
        subjects: list[str],
        bookshelves: list[str],
    ) -> None:
        super().__init__()
        self.id = id
        self.title = title
        self.issued = issued
        self.authors = authors
        self.subjects = subjects
        self.bookshelves = bookshelves
