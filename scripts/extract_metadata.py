import csv
import itertools
import json # For the dump function
import os
import re
from datetime import datetime
from typing import Optional, Tuple, List, Dict # Keep standard typing imports

# --- Updated Type Definitions ---
AuthorId = int
BookId = int

class Author:
    def __init__(self, id: AuthorId, name: str, birth_date: Optional[datetime], death_date: Optional[datetime], books: list[BookId]):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.books = books

class Book:
    def __init__(self, id: BookId, title: str, authors: list[AuthorId], release_date: Optional[datetime], publication_date: Optional[datetime], content_length: int):
        self.id = id
        self.title = title
        self.authors = authors
        self.release_date = release_date
        self.publication_date = publication_date
        self.content_length = content_length

# from authorship_attribution._internal.data_types import Author, AuthorId, Book # User's import

def parse_iso_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def parse_year_to_datetime(year_str: Optional[str]) -> Optional[datetime]:
    if not year_str:
        return None
    cleaned_year_str = re.sub(r'[^\d]', '', year_str)
    if not cleaned_year_str:
        return None
    try:
        year = int(cleaned_year_str)
        if year < 1:
            return None
        return datetime(year, 1, 1)
    except ValueError:
        return None

def parse_author_date_range(date_range_str: Optional[str]) -> Tuple[Optional[datetime], Optional[datetime]]:
    if not date_range_str:
        return None, None
    if "BCE" in date_range_str.upper() or "BC" in date_range_str.upper():
        return None, None
    date_range_str = date_range_str.replace('?', '')
    birth_str: Optional[str] = None
    death_str: Optional[str] = None
    if '-' in date_range_str:
        parts = date_range_str.split('-', 1)
        if parts[0]:
            birth_str = parts[0]
        if parts[1]:
            death_str = parts[1]
    else:
        if re.match(r"^\d{1,4}$", date_range_str):
            birth_str = date_range_str
    return parse_year_to_datetime(birth_str), parse_year_to_datetime(death_str)

def parse_single_author_entry(author_entry_str: str) -> Tuple[Optional[str], Optional[datetime], Optional[datetime]]:
    if not author_entry_str or author_entry_str.lower() == "unknown":
        return None, None, None
    author_entry_str = re.sub(r'\s*\[.*?\]$', '', author_entry_str).strip()
    name_part = author_entry_str
    date_range_part: Optional[str] = None
    match = re.match(r'^(.*?),\s*([\d? BCE-]+)$', author_entry_str)
    if match:
        name_part = match.group(1).strip()
        date_range_part = match.group(2).strip()
    else:
        name_part = author_entry_str.strip()
    if not name_part:
        return None, None, None
    name_part = name_part.rstrip(',').strip()
    birth_date, death_date = parse_author_date_range(date_range_part)
    return name_part, birth_date, death_date

def generate_author_id(name: str) -> AuthorId:
    """Generates an integer ID from the author's name using hash."""
    if not name:
        # Return a consistent ID for "unknown" or empty names,
        # or decide how to handle this case (e.g., skip author).
        # Using 0 for consistency if hash() of empty string is desired.
        return AuthorId(0) # Or hash("unknown_author_placeholder")
    return AuthorId(hash(name))

def read_book_file_content_and_pub_date(book_file_path: str) -> Tuple[str, Optional[datetime], int]:


    publication_date_obj: Optional[datetime] = None
    content_len = 0
    if not os.path.exists(book_file_path):
        print(f"Warning: Book file not found: {book_file_path}")
        return "", None, 0
    try:
        with open(book_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            full_text = f.read()
        pub_match = re.search(r"Original publication:.*?\b(\d{4})\b", full_text, re.IGNORECASE)
        if pub_match:
            publication_date_obj = parse_year_to_datetime(pub_match.group(1))
        if not publication_date_obj:
            release_match = re.search(r"Release date:.*?\[ebook #\d+\]\s*.*?(\b\d{4}\b)", full_text, re.IGNORECASE | re.DOTALL)
            if release_match:
                 year = int(release_match.group(1))
                 if year < 1950:
                     publication_date_obj = parse_year_to_datetime(release_match.group(1))
        start_match = re.search(r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK .*? \*\*\*\s*\n", full_text, re.IGNORECASE)
        end_match = re.search(r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK .*? \*\*\*", full_text, re.IGNORECASE)
        if start_match:
            content_start_index = start_match.end()
            if end_match:
                content_text = full_text[content_start_index:end_match.start()].strip()
            else:
                content_text = full_text[content_start_index:].strip()
            content_len = len(content_text)
        else:
            print(f"Warning: Standard PG start header not found in {book_file_path}")
            lines = full_text.splitlines()
            if len(lines) > 15:
                content_text = "\n".join(lines[15:]).strip()
                content_len = len(content_text)
    except Exception as e:
        print(f"Error reading or parsing book file {book_file_path}: {e}")
        return "", None, 0
    return content_text, publication_date_obj, content_len

def parse_metadata_and_books(csv_filepath: str, books_dir: str, book_output_dir: str, count: Optional[int] = None) -> Tuple[List[Author], List[Book]]:
    """
    Parses the CSV metadata, corresponding book text files, and writes book content to output dir.
    """
    authors_db: Dict[AuthorId, Author] = {}
    books_list: List[Book] = []

    if not os.path.isdir(books_dir):
        print(f"Error: Books directory not found: {books_dir}")
        return [], []
    
    os.makedirs(book_output_dir, exist_ok=True) # Ensure book_output_dir exists

    try:
        with open(csv_filepath, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            enumerator = enumerate(reader)
            if count:
                enumerator = itertools.islice(enumerator, count)
            for row_num, row in enumerator:
                try:
                    book_id_str = row.get("Text#")
                    if not book_id_str:
                        print(f"Warning: Missing 'Text#' in CSV row {row_num + 2}. Skipping.")
                        continue
                    
                    try:
                        book_id = BookId(int(book_id_str))
                    except ValueError:
                        print(f"Warning: Invalid 'Text#' (not an int) in CSV row {row_num + 2}: {book_id_str}. Skipping.")
                        continue
                    
                    book_title = row.get("Title", "Untitled").replace('\n', ' ').strip()
                    ebook_release_date = parse_iso_date(row.get("Issued"))
                    book_author_ids: list[AuthorId] = []
                    raw_authors_str = row.get("Authors", "")

                    if raw_authors_str:
                        author_entries = raw_authors_str.split(';')
                        for entry in author_entries:
                            entry = entry.strip()
                            if not entry:
                                continue
                            name, birth, death = parse_single_author_entry(entry)
                            if name:
                                author_id = generate_author_id(name)
                                if author_id not in authors_db:
                                    authors_db[author_id] = Author(
                                        id=author_id,
                                        name=name,
                                        birth_date=birth,
                                        death_date=death,
                                        books=[] # Initialize with empty list
                                    )
                                if book_id not in authors_db[author_id].books:
                                    authors_db[author_id].books.append(book_id)
                                if author_id not in book_author_ids:
                                    book_author_ids.append(author_id)
                    
                    book_file_path = os.path.join(books_dir, f"pg{book_id_str}.txt")
                    content, original_publication_date, content_len = \
                        read_book_file_content_and_pub_date(book_file_path)

                    # Write book content to its own file
                    current_book_output_path = os.path.join(book_output_dir, str(book_id))
                    os.makedirs(current_book_output_path, exist_ok=True)
                    with open(os.path.join(current_book_output_path, "original.txt"), 'w', encoding='utf-8') as bf:
                        bf.write(content)

                    # Create Book object (note: content is stored in memory here AND written to file)
                    # If memory is a concern for very large books/datasets, you might choose
                    # not to store book.content in the Book object after writing it.
                    book = Book(
                        id=book_id,
                        title=book_title,
                        authors=book_author_ids,
                        release_date=ebook_release_date, 
                        publication_date=original_publication_date,
                        content_length=content_len
                    )
                    books_list.append(book)

                except Exception as e:
                    print(f"Error processing CSV row {row_num + 2} (Book ID {book_id_str}): {e}")
                    import traceback
                    traceback.print_exc()

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred while processing CSV: {e}")
        return [], []

    return list(authors_db.values()), books_list


def dump(path: str, objects: List[object]):
    """Helper to dump list of objects to JSON, converting objects to dicts."""
    # Ensure output directory for dump exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding='utf-8') as f:
        # Handle datetime objects for JSON serialization
        def datetime_converter(o):
            if isinstance(o, datetime):
                return o.isoformat()
        json.dump([item.__dict__ for item in objects], f, indent=4, sort_keys=True, default=datetime_converter)

if __name__ == "__main__":
    BOOKS_CSV = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/All/pg_catalog_fixed.csv"
    BOOKS_DIR = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/All/epub/"
    BOOK_OUTPUT_PROCESSED_DIR = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/Short/processed_texts/"
    JSON_OUTPUT_DIR = "/home/wannes/Documenten/personal/Tools/Project-gutenberg/Short"

    os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
    os.makedirs(BOOK_OUTPUT_PROCESSED_DIR, exist_ok=True)

    BOOKS_JSON_FILE = os.path.join(JSON_OUTPUT_DIR, "books.json")
    AUTHORS_JSON_FILE = os.path.join(JSON_OUTPUT_DIR, "authors.json")

    all_authors, all_books = parse_metadata_and_books(
        BOOKS_CSV,
        BOOKS_DIR,
        BOOK_OUTPUT_PROCESSED_DIR,
    )
    
    dump(AUTHORS_JSON_FILE, all_authors)
    dump(BOOKS_JSON_FILE, all_books)
    print(f"JSON data dumped to '{JSON_OUTPUT_DIR}'.")