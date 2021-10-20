import os
import pyttsx3
from io import BytesIO
from pydub import AudioSegment


def convert(text):
    if not hasattr(convert, "engine"):
        convert.engine = pyttsx3.init()
    if not hasattr(convert, "counter"):
        convert.counter = 0

    convert.counter += 1
    filename = str(convert.counter)+'.wav'

    convert.engine.save_to_file(text, filename)
    convert.engine.runAndWait()
    audio = AudioSegment.from_wav(filename)
    os.remove(filename)

    return audio
