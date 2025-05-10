from datetime import datetime
import json
from os import path
import os
from typing import List

from authorship_attribution._internal.data_types import OldAuthor, OldBook


def parse_json_objects(path: str, T: type) -> List[object]:
    with open(path, "r") as f:
        return json.load(f, object_hook=lambda d: T(**d))


def write_json_objects(path: str, objects: List[object]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            [vars(item) for item in objects],
            f,
            indent=4,
            default=lambda o: o.isoformat() if isinstance(o, datetime) else None,
        )


def read_book(
    book_dir: str,
    book_id: int,
) -> str:
    book_path = path.join(book_dir, str(book_id), "original.txt")
    with open(book_path, "r") as f:
        return f.read()


def write_book(
    author_id: int,
    out_dir: str,
    book_id: int,
    content: str,
):
    book_file_path = path.join(out_dir, str(author_id), str(book_id), "original.txt")
    os.makedirs(os.path.dirname(book_file_path), exist_ok=True)
    with open(book_file_path, "w") as f:
        f.write(content)


def organise_data(
    books: list[OldBook], authors: list[OldAuthor], in_book_dir: str, out_book_dir: str
):
    authors_by_id = {author.id: author for author in authors}
    for book in books:
        if len(book.authors) != 1:
            continue
        for author_id in book.authors:
            if author_id not in authors_by_id:
                continue
            if authors_by_id[author_id].birth_date is None:
                continue
            if authors_by_id[author_id].death_date is None:
                continue
            author_dir = path.join(out_book_dir, str(author_id))
            os.makedirs(author_dir, exist_ok=True)
            book_content = read_book(in_book_dir, book.id)
            write_book(author_id, out_book_dir, book.id, book_content)


if __name__ == "__main__":
    IN_DIR = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/processed/"
    IN_BOOKS_JSON_FILE = path.join(IN_DIR, "books.json")
    IN_AUTHORS_JSON_FILE = path.join(IN_DIR, "authors.json")
    IN_BOOKS_DIR = path.join(IN_DIR, "books")

    BOOKS = parse_json_objects(IN_BOOKS_JSON_FILE, OldBook)
    AUTHORS = parse_json_objects(IN_AUTHORS_JSON_FILE, OldAuthor)

    OUT_DIR = "out"
    OUT_BOOKS_JSON_FILE = path.join(OUT_DIR, "books.json")
    OUT_AUTHORS_JSON_FILE = path.join(OUT_DIR, "authors.json")
    OUT_BOOKS_DIR = path.join(OUT_DIR, "books")

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(OUT_BOOKS_DIR, exist_ok=True)

    write_json_objects(OUT_AUTHORS_JSON_FILE, AUTHORS)
    write_json_objects(OUT_BOOKS_JSON_FILE, BOOKS)

    organise_data(BOOKS, AUTHORS, IN_BOOKS_DIR, OUT_BOOKS_DIR)
