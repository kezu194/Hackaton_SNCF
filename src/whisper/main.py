import whisper as wh

from src.whisper import load_file
import warnings

warnings.filterwarnings("ignore")

# Execute this script OR use the command line from the projet root folder
# pip install -r src/whisper/requirements.txt
# whisper assets/sounds/0087001479-DCT-20230810-081529-468ca229-718b-4244-b0bb-bfc60a365a77.mp3 --language French -o assets/results -f txt
#                   ^-- The audio file to transcribe                        The language of the audio --^              ^-- Output folder and type of output

MODEL = wh.load_model("large")


def transcribe(filename=load_file.get_first_file(), use_small=False):
    model = MODEL if not use_small else wh.load_model("small")
    result = model.transcribe(str(filename))
    return result["text"]
