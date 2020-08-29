from math import exp


def number_code_from_letter_code(letter_code, alphabet):
    return [alphabet.letters_to_position[letter] for letter in letter_code]


def is_word_end(text, index):
    try:
        return index in text.ends_of_words
    except AttributeError:

        return False


def get_n_gram_generator_at_i_left(text, n, i):
    gram = ""
    k = i
    t = k
    while i - t < n and k >= 0:
        gram = text[k] + gram
        k -= 1
        t -= 1
        if is_word_end(text, k):
            stripped = text.stripped_part[text.ends_of_words[k]]
            j = len(stripped) - 1
            while i - t < n and j >= 0:
                gram = stripped[j] + gram
                t -= 1
                j -= 1
    if gram:
        return gram[:-1]
    return gram


def get_n_gram_generator_at_i_right(text, n, i):
    gram = ""
    k = i
    t = i
    while t - i < n and k < len(text):
        gram += text[k]
        k += 1
        t += 1
        if is_word_end(text, k - 1):
            stripped = text.stripped_part[text.ends_of_words[k-1]]
            j = 0
            while t - i < n and j < len(stripped):
                gram += stripped[j]
                t += 1
                j += 1
    return gram


def get_n_gram_generator_at_i(text, n, i):
    if i < 0 or i >= len(text):
        return None
    gram = get_n_gram_generator_at_i_left(text, n, i) + get_n_gram_generator_at_i_right(text, n, i)
    if len(gram) < n:
        return None
    return gram


def get_n_grams_with_i(text, n, i):
    generator = get_n_gram_generator_at_i(text, n, i)
    if generator:
        return [generator[i:i+n] for i in range(len(generator) - n + 1)]
    return []


def calculate_n_gram_frequencies(text, n):
    frequencies_dict = {}
    current_gram = ""
    if is_word_end(text, -1):
        stripped_beginning = text.stripped_part[text.ends_of_words[-1]]
        for i in range(len(stripped_beginning)):
            current_gram += stripped_beginning[i]
            if len(current_gram) > n:
                current_gram = current_gram[1:]
            if len(current_gram) == n:
                try:
                    frequencies_dict[current_gram] += 1
                except KeyError:
                    frequencies_dict[current_gram] = 1
    for i in range(len(text)):
        current_gram += text[i]
        if len(current_gram) > n:
            current_gram = current_gram[1:]
        if len(current_gram) == n:
            try:
                frequencies_dict[current_gram] += 1
            except KeyError:
                frequencies_dict[current_gram] = 1
        if is_word_end(text, i):
            stripped = text.stripped_part[text.ends_of_words[i]]
            for j in range(len(stripped)):
                current_gram += stripped[j]
                if len(current_gram) > n:
                    current_gram = current_gram[1:]
                if len(current_gram) == n:
                    try:
                        frequencies_dict[current_gram] += 1
                    except KeyError:
                        frequencies_dict[current_gram] = 1
    return frequencies_dict


def calculate_n_gram_log_weight(frequencies, log_distribution):
    result = 0
    for i in frequencies:
        try:
            result += log_distribution[i]*frequencies[i]
        except KeyError:
            pass
    return result


def get_frequencies_change(old_frequencies, new_frequencies):
    frequencies_change = {}
    for i in old_frequencies:
        if old_frequencies[i] != new_frequencies[i]:
            frequencies_change[i] = new_frequencies[i] - old_frequencies[i]
    return frequencies_change


def calculate_log_weight_change(frequencies_change, log_distribution):
    result = 0
    for i in frequencies_change:
        try:
            result += log_distribution[i]*frequencies_change[i]
        except KeyError:
            pass
    return result


def update_frequency(frequency, frequency_change):
    for i in frequency_change:
        try:
            frequency[i] += frequency_change[i]
        except KeyError:
            frequency[i] = frequency_change[i]


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i


def add_gram_to_frequency_change(gram, frequencies_change):
    if not gram:
        return
    try:
        frequencies_change[gram] += 1
    except KeyError:
        frequencies_change[gram] = 1


def subtract_gram_from_frequency_change(gram, frequencies_change):
    if not gram:
        return
    try:
        frequencies_change[gram] -= 1
    except KeyError:
        frequencies_change[gram] = -1


def get_bigrams_in_coords(text, i):
    bigrams = []
    if i == 0 and is_word_end(text, -1):
        beginning = text.stripped_part[text.ends_of_words[-1]]
        bigrams.append(beginning[-1] + text[i])
    if not is_word_end(text, i) and i + 1 < len(text):
        bigrams.append(text[i]+text[i+1])
        return bigrams
    stripped_index = text.ends_of_words[i]
    if text.stripped_part[stripped_index]:
        bigrams.append(text[i] + text.stripped_part[stripped_index][0])
        if i + 1 < len(text):
            bigrams.append(text.stripped_part[stripped_index][-1] + text[i+1])
    return bigrams


def expected_value(log_frequencies, text_length):
    normalizer = 0
    expected = 0
    for i in log_frequencies:
        normalizer += exp(log_frequencies[i])
    for i in log_frequencies:
        expected += log_frequencies[i]*exp(log_frequencies)
    return (expected/normalizer)*text_length


def consistency_vigenere(guessed_key, real_key, alphabet):
    guessed_copy = guessed_key[:]
    real_copy = real_key[:]
    while len(guessed_copy) != len(real_copy):
        if len(guessed_copy) > len(real_copy):
            real_copy += real_key
        else:
            guessed_copy += guessed_key
    accuracy = 0
    for i in range(len(guessed_copy)):
        if not (guessed_copy[i] - real_copy[i]) % alphabet.length:
            accuracy += 1

    return accuracy/len(guessed_copy)


def consistency_vigenere_extended(guessed_key, real_key, alphabet):
    guessed_copy = guessed_key[:]
    real_copy = real_key[:]
    while len(guessed_copy) != len(real_copy):
        if len(guessed_copy) > len(real_copy):
            real_copy += real_key
        else:
            guessed_copy += guessed_key
    accuracy = 0
    for i in range(len(guessed_copy)):
        if not (guessed_copy[i][0] - real_copy[i][0]) % alphabet.length and \
                not (guessed_copy[i][1] - real_copy[i][1]) % alphabet.length:
            accuracy += 1
    return accuracy/len(guessed_copy)


def consistency(guessed_key, real_key, alphabet):
    try:
        return consistency_vigenere(guessed_key, real_key, alphabet)
    except TypeError:
        return consistency_vigenere_extended(guessed_key, real_key, alphabet)


def get_piece_on_i_coordinate(text, i, key_length):
    piece = []
    for coord in range(i, len(text), key_length):
        piece.append(text[coord])
    return piece
