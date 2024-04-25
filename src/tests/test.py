from src.utils import extract_data
from src.transcription import AUDIO_DIR, transcribe
from src.text_comparaison import compare_sentences

data: list[dict[str, str]] = extract_data()

for element in data:
    filename = AUDIO_DIR / element["filename"]
    transcription = transcribe(filename)

    similarities_rate = compare_sentences(element["sentence"], [transcription])

    print(filename, f"{similarities_rate[0]}%")

