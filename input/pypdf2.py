import os
import PyPDF2
import input.utils


def convert(filename):
    text = [os.path.basename(filename)]

    with open(filename, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        for p in range(pdf.getNumPages()):
            page = pdf.getPage(p)
            page_text = page.extractText()
            text += input.utils.split_text(page_text)

    return text
