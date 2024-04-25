import whisper as wh

from pathlib import Path
import os
import warnings

warnings.filterwarnings("ignore")

# Execute this script OR use the command line from the projet root folder
# pip install -r src/whisper/requirements.txt
# whisper assets/sounds/0087001479-DCT-20230810-081529-468ca229-718b-4244-b0bb-bfc60a365a77.mp3 --language French -o assets/results -f txt
#                   ^-- The audio file to transcribe                        The language of the audio --^              ^-- Output folder and type of output

AUDIO_DIR = Path(__file__).parent.parent.parent.joinpath('assets/sounds')


def get_first_file() -> Path:
    """
    Get first file path from the assets/sounds directory.

    :return: The Path of the file
    """

    first_file = os.listdir(AUDIO_DIR)[0]
    file_path = AUDIO_DIR / first_file
    return file_path


MODEL = wh.load_model("large")


def transcribe(filename=get_first_file(), use_small=False):
    model = MODEL if not use_small else wh.load_model("small")
    result = model.transcribe(str(filename))
    return result["text"]
