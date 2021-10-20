import os
import ebooklib
from ebooklib import epub
import html2text
import input.utils


def convert(filename):
    text = [os.path.basename(filename)]

    book = epub.read_epub(filename)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            tmp_text = html2text.html2text(item.get_content().decode())
            text += input.utils.split_text(tmp_text)

    return text
