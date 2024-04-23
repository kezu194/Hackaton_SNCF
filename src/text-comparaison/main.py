from utils import remove_stop_words, list_words, count_words, calculate_similarities, list_letters, count_letters


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

print(compare_sentences(text1, [text2]))


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


print(compare_words("Chien", ["Chat", "Oiseau", "Cheval", "Canard", "cHieN"]))
