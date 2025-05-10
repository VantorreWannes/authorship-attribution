from datetime import datetime
import json
import os
from typing import List, Optional
from authorship_attribution._internal.data_types import (
    Author,
    Book,
    DateRange,
    OldAuthor,
    OldBook,
)


def parse_json_objects(path: str, T: type) -> List[object]:
    with open(path, "r") as f:
        return json.load(f, object_hook=lambda d: T(**d))


def write_json_objects(path: str, objects: List[object]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            [dict(item) for item in objects],
            f,
            indent=4,
        )


def read_book(
    book_dir: str,
    book_id: int,
) -> str:
    book_path = os.path.join(book_dir, str(book_id), "original.txt")
    with open(book_path, "r") as f:
        return f.read()


def write_book(
    book_dir: str,
    book_id: int,
    content: str,
):
    book_path = os.path.join(book_dir, str(book_id), "original.txt")
    os.makedirs(os.path.dirname(book_path), exist_ok=True)
    with open(book_path, "w") as f:
        f.write(content)


def get_lifetime(
    birth_date: Optional[datetime], death_date: Optional[datetime]
) -> DateRange:
    if birth_date is None or death_date is None:
        return None
    return DateRange(birth_date, death_date)


def organise_authors(old_authors: list[OldAuthor]) -> list[Author]:
    authors = list()
    for old_author in old_authors:
        id = old_author.id
        name = old_author.name
        lifetime = get_lifetime(old_author.birth_date, old_author.death_date)
        book_ids = list(old_author.books)
        author = Author(id, name, lifetime, book_ids)
        authors.append(author)
    return authors


def organise_books(
    old_books: list[OldBook],
    in_book_dir: str,
    out_book_dir: str,
) -> list[Book]:
    books = list()
    for old_book in old_books:
        id = old_book.id
        title = old_book.title
        author_ids = list(old_book.authors)
        release_date = old_book.release_date
        publication_date = old_book.publication_date
        content_length = old_book.content_length
        folder_path = os.path.join(out_book_dir, str(id))
        content = read_book(in_book_dir, id)
        write_book(out_book_dir, id, content)
        book = Book(
            id,
            title,
            author_ids,
            release_date,
            publication_date,
            content_length,
            folder_path,
        )
        books.append(book)
    return books


if __name__ == "__main__":
    IN_DIR = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/processed/"
    IN_BOOKS_JSON_FILE = os.path.join(IN_DIR, "books.json")
    IN_AUTHORS_JSON_FILE = os.path.join(IN_DIR, "authors.json")
    IN_BOOKS_DIR = os.path.join(IN_DIR, "books")

    OLD_BOOKS = parse_json_objects(IN_BOOKS_JSON_FILE, OldBook)
    OLD_AUTHORS = parse_json_objects(IN_AUTHORS_JSON_FILE, OldAuthor)

    OUT_DIR = "data"
    OUT_BOOKS_JSON_FILE = os.path.join(OUT_DIR, "books.json")
    OUT_AUTHORS_JSON_FILE = os.path.join(OUT_DIR, "authors.json")
    OUT_BOOKS_DIR = os.path.join(OUT_DIR, "books")

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(OUT_BOOKS_DIR, exist_ok=True)

    BOOKS = organise_books(OLD_BOOKS, IN_BOOKS_DIR, OUT_BOOKS_DIR)
    AUTHORS = organise_authors(OLD_AUTHORS)

    write_json_objects(OUT_AUTHORS_JSON_FILE, AUTHORS)
    write_json_objects(OUT_BOOKS_JSON_FILE, BOOKS)
