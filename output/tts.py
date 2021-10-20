from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from io import BytesIO
from pydub import AudioSegment


def convert(text):
    model_path = 'tts_models--fr--mai--tacotron2-DDC/model.pth.tar'
    config_path = 'tts_models--fr--mai--tacotron2-DDC/config.json'

    if not hasattr(convert, "synthesizer"):
        convert.synthesizer = Synthesizer(model_path,
                                  config_path,
                                  use_cuda=False)

    wavs = convert.synthesizer.tts(text)

    audio = BytesIO()
    convert.synthesizer.save_wav(wavs, audio)
    audio.seek(0)

    return AudioSegment.from_wav(audio)
