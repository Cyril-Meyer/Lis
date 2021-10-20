import os
import textract
import input.utils


def convert(filename):
    text = [os.path.basename(filename)]

    tmp_text = textract.process(filename).decode()
    text += input.utils.split_text(tmp_text)

    return text
