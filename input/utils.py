import os
import re

def split_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(' +', ' ', text)

    text = text.replace('.', '.')
    text = text.replace('?', '?.')
    text = text.replace('!', '!.')

    return text.split(".")


def read_txt(filename):
    text = [os.path.basename(filename)]

    with open(filename, 'r', encoding="utf-8") as f:
        tmp_text = f.read()
        text += split_text(tmp_text)

    return text
