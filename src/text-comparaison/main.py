from math import sqrt


def count_letters(word, dict_letter):
    copy_dict = dict_letter.copy()
    for letter in word:
        copy_dict[letter] += 1
    return copy_dict


def list_letters(words):
    dict_letter = {}
    for word in words:
        for letter in word:
            if letter not in dict_letter:
                dict_letter[letter] = 0
    return dict_letter


def calculate_similarities(dict_word_1, dict_word_2):
    list_word_1 = [value for value in dict_word_1.values()]
    list_word_2 = [value for value in dict_word_2.values()]
    total = 0
    for index, _ in enumerate(list_word_1):
        total += list_word_1[index] * list_word_2[index]

    square_total = 0
    for value in list_word_1:
        square_total += value ** 2
    magnitude_1 = sqrt(square_total)
    square_total = 0
    for value in list_word_2:
        square_total += value ** 2
    magnitude_2 = sqrt(square_total)
    return total / (magnitude_1 * magnitude_2)


def compare_words(sentence1, sentence2):
    dict_letters = list_letters([sentence1, sentence2])
    list_letters_count = []
    for sentence in [sentence1, sentence2]:
        list_letters_count.append(count_letters(sentence, dict_letters))
    print(calculate_similarities(list_letters_count[0], list_letters_count[1]))


compare_words("transsino.com", "transilien.com")
