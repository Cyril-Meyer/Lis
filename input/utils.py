import re

def split_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(' +', ' ', text)

    text = text.replace('.', '.')
    text = text.replace('?', '?.')
    text = text.replace('!', '!.')

    return text.split(".")