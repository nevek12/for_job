import os
import re

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    text = text[start:].lstrip()
    s = ''
    v = []
    for i in range(len(text)):
        s += text[i]
        if text[i] in '.?!:;,' and len(s) <= size:
            v.append(s)
        if len(s) > size:
            if text[i] in '.?!:;,' and text[i-1] in '.?!:;,':
               return v[-3], len(v[-3])
            return v[-1], len(v[-1])
    return v[-1], len(v[-1])
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
        c = re.sub(r"\s", " ", c)
        out_c = re.split(r"[()]", c)
        return _get_part_text(out_c[0], len(out_c)-1, PAGE_SIZE)

prepare_book('book.txt')
print(book)