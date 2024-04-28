from math import sqrt
from typing import Any

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

import whisper as wh

import warnings
import csv

warnings.filterwarnings("ignore")


# Execute this script OR use the command line from the projet root folder
# pip install -r src/whisper/requirements.txt
# whisper assets/sounds/0087001479-DCT-20230810-081529-468ca229-718b-4244-b0bb-bfc60a365a77.mp3 --language French -o assets/results -f txt
#                   ^-- The audio file to transcribe                        The language of the audio --^              ^-- Output folder and type of output


def extract_data() -> list[dict[str, str]]:
    """
    Extract data from CSV file
    :return:
    """
    with open("./assets/data.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        header = next(spamreader)

        list_results = []
        for row in spamreader:
            list_results.append({
                'filename': row[-1],
                'sentence': row[-3]
            })
        return list_results


def update_all_location_position(old_word: str, new_word: str, list_location: list[dict[str, Any]]):
    size = len(new_word) - len(old_word)
    for location in list_location:
        location["start"] += size
        location["end"] += size


def transcribe(filename) -> str:
    transcription_fr = MODEL.transcribe(audio=str(filename), language="fr", task="transcribe")["text"]

    # Fix location errors
    list_locations = detect_locations(transcription_fr)
    for location in list_locations:
        if location["word"] == "Paris Gardinard":
            transcription_fr = transcription_fr[:location["start"]] + " Gare du Nord" + transcription_fr[location["end"]:]
            update_all_location_position(location["word"], " Gare du Nord", list_locations)
        if location["word"].lower() not in ["paris", "voie", "lille"]:
            close_location, score = compare_locations_with_dataset(location["word"], LIST_LOCATION)
            if score >= 90:
                print(location, close_location, score)
                transcription_fr = transcription_fr[:location["start"]] + " " + close_location + transcription_fr[location["end"]:]
                update_all_location_position(location["word"], close_location, list_locations)
            else:
                print(location, close_location, score, "Pas de localisation exact trouvé")

    return transcription_fr


def detect_locations(sentence):
    # Charger le tokenizer et le modèle NER
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner")

    # Créer un pipeline NER avec le modèle et le tokenizer
    nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    # Utiliser le pipeline pour effectuer la reconnaissance d'entités nommées sur le texte
    result = nlp(sentence)

    # Initialiser une liste pour stocker les informations sur les localisations détectées
    locations = []

    # Parcourir la liste des entités nommées identifiées
    for entity in result:
        # Vérifier si l'entité est une localisation
        if entity['entity_group'] == 'LOC':
            # Stocker les informations sur la localisation dans la liste
            location_info = {
                'word': entity['word'],
                'start': entity['start'],
                'end': entity['end'],
                'score': entity['score']
            }
            locations.append(location_info)
        print(entity)

    return locations


def compare_locations_with_dataset(location: str, dataset: list[str]) -> tuple[str, float]:
    # Comparer la localisation avec chaque localisation de l'ensemble de données
    similarity_scores: list[float] = compare_words(location, dataset)
    max_similarity = max(similarity_scores)

    # Trouver la localisation avec le score de similarité le plus élevé
    return dataset[similarity_scores.index(max_similarity)], max_similarity


def compare_sentences(sentence_model: str, list_sentence_to_compare_with: list[str]) -> list[float]:
    """
    Compare a sentence/word with a list of words/sentences.

    :param sentence_model:
    :param list_sentence_to_compare_with:
    :return:
    """
    # Remove stop words
    sentence_model = remove_stop_words(sentence_model)
    for index, sentence in enumerate(list_sentence_to_compare_with):
        list_sentence_to_compare_with[index] = remove_stop_words(sentence)

    # Get the list of all words in sentences
    dict_letters = list_words([sentence_model] + list_sentence_to_compare_with)

    # Count the number of occurrence of each word in each sentence then calculate the similarities
    model_count = count_words(sentence_model, dict_letters)
    list_result = []
    for sentence in list_sentence_to_compare_with:
        sentence_count = count_words(sentence, dict_letters)
        list_result.append(calculate_similarities(model_count, sentence_count) * 100)
    return list_result


def compare_words(model_word: str, list_word_to_compare_with: list[str]) -> list[float]:
    """
    Compare a word with a list of words and return a percentage of similarity for each word.

    :param model_word:
    :param list_word_to_compare_with:
    :return:
    """
    # Remove stop words
    model_word = remove_stop_words(model_word)
    for index, sentence in enumerate(list_word_to_compare_with):
        list_word_to_compare_with[index] = remove_stop_words(sentence)

    # Enumerate all letter in the words
    dict_letters = list_letters([model_word] + list_word_to_compare_with)

    # Count the number of letter for each word
    dict_word_1 = count_letters(model_word, dict_letters)
    list_result = []
    for word in list_word_to_compare_with:
        count = count_letters(word, dict_letters)
        list_result.append(calculate_similarities(dict_word_1, count) * 100)
    return list_result


def remove_stop_words(sentence: str) -> str:
    """
    Remove all stop words from a sentence.

    :param sentence:
    :return:
    """
    new_sentence: str = ""
    for word in word_tokenize(sentence, language="french"):
        if word not in STOP_WORDS:
            new_sentence += word + " "
    return new_sentence


def count_words(sentence: str, dict_letter: dict[str, int]) -> dict[str, int]:
    """
    Count the number of words in a sentence and store in a dictionary.

    :param sentence:
    :param dict_letter:
    :return:
    """
    copy_dict: dict[str, int] = dict_letter.copy()
    for word in word_tokenize(sentence, language="french"):
        copy_dict[word.lower()] += 1
    return copy_dict


def list_words(list_sentence: list[str]) -> dict[str, int]:
    """
    List all word present in the given sentences.

    :param list_sentence:
    :return:
    """
    dict_letter: dict[str, int] = {}
    # For each sentence given
    for sentence in list_sentence:
        # For each word in the sentence
        for word in word_tokenize(sentence, language="french"):
            # Add in the dict if word not in already in dict
            if word.lower() not in dict_letter:
                dict_letter[word.lower()] = 0
    return dict_letter


def calculate_similarities(dict_word_1: dict[str, int], dict_word_2: dict[str, int]) -> float:
    list_word_1: list[int] = [value for value in dict_word_1.values()]
    list_word_2: list[int] = [value for value in dict_word_2.values()]
    total: int = 0
    for index, _ in enumerate(list_word_1):
        total += list_word_1[index] * list_word_2[index]
    return total / (get_magnitude(list_word_1) * get_magnitude(list_word_2))


def get_magnitude(list_value: list[int]) -> float:
    square_total: int = 0
    for value in list_value:
        square_total += value ** 2
    return sqrt(square_total)


def list_letters(list_words: list[str]) -> dict[str, int]:
    dict_letter: dict[str, int] = {}
    for word in list_words:
        for letter in word:
            if letter.lower() not in dict_letter:
                dict_letter[letter.lower()] = 0
    return dict_letter


def count_letters(word: str, dict_letter: dict[str, int]) -> dict[str, int]:
    copy_dict: dict[str, int] = dict_letter.copy()
    for letter in word:
        copy_dict[letter.lower()] += 1
    return copy_dict


from transformers import MarianMTModel, MarianTokenizer


def translate_to_spanish(text: str):
    model_name = "Helsinki-NLP/opus-mt-en-es"

    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    res = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return res[0]


def translate_to_english(text: str):
    model_name = "Helsinki-NLP/opus-mt-fr-en"

    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    res = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return res[0]

# LIST_LOCATION = extract_location("./assets/liste-des-gares-voyageurs.csv")


MODEL = wh.load_model("small")
# nltk.download('punkt')
# nltk.download('stopwords')
STOP_WORDS = stopwords.words('french')


def get_list_gare():
    with open("frequentation-gares.csv") as file:
        csvreader = csv.reader(file, delimiter=";")
        header = next(csvreader)
        list_gare = []
        for row in csvreader:
            if int(row[1]) >= 1000000:
                list_gare.append(row[0])
    return list_gare


# Get the list of popular gare station
LIST_LOCATION = list(set(get_list_gare()))


def test(audio_path):
    transcription_fr: str = transcribe(audio_path).removeprefix(" ")  # Remove empty space at beginning
    transcription_en: str = translate_to_english(transcription_fr)
    transcription_es: str = translate_to_spanish(transcription_en)

    return transcription_fr, transcription_en, transcription_es
