import os
import pdfplumber
import input.utils


def convert(filename):
    text = [os.path.basename(filename)]

    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            text += input.utils.split_text(page_text)

    return text
