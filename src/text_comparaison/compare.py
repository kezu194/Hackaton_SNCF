from src.text_comparaison.libs import remove_stop_words, list_words, count_words, calculate_similarities, list_letters, count_letters


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
