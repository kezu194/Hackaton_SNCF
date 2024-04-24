from math import sqrt
from nltk.tokenize import word_tokenize
from stop_word import STOP_WORDS


def remove_stop_words(sentence: str) -> str:
    """
    Remove all stop words from a sentence.

    :param sentence:
    :return:
    """
    new_sentence: str = ""
    for word in word_tokenize(sentence):
        if word == ",":
            new_sentence = new_sentence.removesuffix(" ")
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
