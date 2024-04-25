from math import sqrt
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

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

import csv

DATA_CSV = Path(__file__).joinpath("assets/data.csv")


def extract_data() -> list[dict[str, str]]:
    """
    Extract data from CSV file
    :return:
    """
    with open(DATA_CSV) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        header = next(spamreader)

        list_results = []
        for row in spamreader:
            list_results.append({
                'filename': row[-1],
                'sentence': row[-3]
            })
        return list_results


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


nltk.download('punkt')
nltk.download('stopwords')
STOP_WORDS = stopwords.words('french')


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

    return locations


def compare_locations_with_dataset(locations, dataset):
    # Initialiser une liste pour stocker les pourcentages de similarité
    similarities = []

    # Comparer chaque localisation avec les localisations de l'ensemble de données
    for location in locations:
        # Comparer la localisation avec chaque localisation de l'ensemble de données
        similarity_scores = compare_sentences(location['word'], dataset)

        # Ajouter le pourcentage de similarité le plus élevé à la liste des similarités
        max_similarity = max(similarity_scores)
        similarities.append(max_similarity)

    return similarities


# Test de la fonction avec une phrase
# sentence = "Apple est créée le 1er avril 1976 dans le garage de la maison d'enfance de Steve Jobs à Los Altos en Californie par Steve Jobs, Steve Wozniak et Ronald Wayne14, puis constituée sous forme de société le 3 janvier 1977 à l'origine sous le nom d'Apple Computer, mais pour ses 30 ans et pour refléter la diversification de ses produits, le mot « computer » est retiré le 9 janvier 2015."
# locations = detect_locations(sentence)
#
# # Exemple de dataset de localisations à comparer
# dataset = ["Los Altos", "Californie", "Beauvais", "Paris"]
#
# # Comparer les localisations détectées avec le dataset
# similarities = compare_locations_with_dataset(locations, dataset)
#
# # Afficher les résultats
# for i, location in enumerate(locations):
#     print(f"Localisation: {location['word']}")
#     print(f"Début: {location['start']}, Fin: {location['end']}")
#     print(f"Score de confiance: {location['score']}")
#     print(f"Pourcentage de similarité avec le dataset: {similarities[i]}%")


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
    for word in word_tokenize(sentence):
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
    for word in word_tokenize(sentence):
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
        for word in word_tokenize(sentence):
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


if __name__ == '__main__':

    data: list[dict[str, str]] = extract_data()

    for element in data:
        filename = AUDIO_DIR / element["filename"]
        transcription = transcribe(filename)

        similarities_rate = compare_sentences(element["sentence"], [transcription])

        print(filename, f"{similarities_rate[0]}%")
