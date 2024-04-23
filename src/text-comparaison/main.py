from math import sqrt
from nltk.tokenize import word_tokenize
from stop_word import STOP_WORDS


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


def calculate_similarities(dict_word_1: dict[str, int], dict_word_2: dict[str, int]):
    list_word_1: list[int] = [value for value in dict_word_1.values()]
    list_word_2: list[int] = [value for value in dict_word_2.values()]
    total: int = 0
    for index, _ in enumerate(list_word_1):
        total += list_word_1[index] * list_word_2[index]
    return total / (get_magnitude(list_word_1) * get_magnitude(list_word_2))


def get_magnitude(list_value: list[int]) -> float:
    square_total = 0
    for value in list_value:
        square_total += value ** 2
    return sqrt(square_total)


def compare_words(sentence_model: str, list_sentence_to_compare_with: list[str]) -> None:
    """
    Compare a sentence/word with a list of words/sentences.

    :param sentence_model:
    :param list_sentence_to_compare_with:
    :return:
    """
    sentence_model = remove_stop_words(sentence_model)
    for index, sentence in enumerate(list_sentence_to_compare_with):
        list_sentence_to_compare_with[index] = remove_stop_words(sentence)
    dict_letters = list_words([sentence_model] + list_sentence_to_compare_with)
    model_count = count_words(sentence_model, dict_letters)
    for sentence in list_sentence_to_compare_with:
        sentence_count = count_words(sentence, dict_letters)
        print(calculate_similarities(model_count, sentence_count) * 100, "%")


def remove_stop_words(sentence):
    new_sentence = ""
    for word in word_tokenize(sentence):
        if word == ",":
            new_sentence = new_sentence.removesuffix(" ")
        if word not in STOP_WORDS:
            new_sentence += word + " "
    return new_sentence


text1 = """Flash, info, trafic, ligne EP, madame, monsieur, bonjour et bienvenue en gare. Il est 17h31, alors pour 
moi, je vais vous faire un point sur la circulation. Actuellement, le trafic est fini sur l'ensemble de la ligne, 
mais je vous rappelle que jusqu'au 27 août, il n'y a pas de service jusqu'au 20 août. Le trafic est interrompu entre 
Fontaine-Méchelon et Massif-Alejo. Et jusqu'au 25 août, le trafic est interrompu entre Boulogne et Néroposon. 
Poursuivons en temps réel l'évolution de votre ligne. Je vous invite à consulter les applications Ile-de-France 
Mobilité, les sites transsino.com, ratp.fr, sncfconnect ou votre appli de mobilité. Je vous souhaite à tous et à 
toutes une agréable journée et un bon voyage."""
text2 = """Flash info trafic ligne B Madame, Monsieur, Bonjour et bienvenue en gare. Il est 17 h 31 l'heure pour moi 
de vous faire un point sur la circulation. Actuellement le trafic est fluide sur l'ensemble de la ligne mais je vous 
rappelle que jusqu'au 27 août Bagne n'est pas desservie jusqu au 20 août, le trafic est interrompu entre Fontaine 
Michalon, Massy Palaiseau et jusqu'au 25 août, le trafic est interrompu entre  Blois,Rennes et Robinson  pour suivre 
en temps réel l'évolution de votre ligne, je vous invite à consulter les applications Île-de-France mobilités des 
site Transilien.com, ratp.fr SNCF connectant votre appli de Mobilités, je vous souhaite à tous et à toutes une 
agréable journée, un pour voyage."""

compare_words(text1, [text2])
compare_words("Chat", ["Chien"])
