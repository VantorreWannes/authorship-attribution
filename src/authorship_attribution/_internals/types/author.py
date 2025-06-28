from authorship_attribution._internals.types.aliases import BookId, Id


class Author:
    def __init__(self, id: Id, name: str, books: list[BookId]) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.books = books
