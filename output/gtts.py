from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment


def convert(text):
    audio = BytesIO()

    tts = gTTS(text, lang='fr')
    # tts.save('audio.mp3')
    tts.write_to_fp(audio)
    audio.seek(0)

    return AudioSegment.from_mp3(audio)
