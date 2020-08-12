from math import exp


def get_zero_frequency(frequencies):
    return min(frequencies.values())/2


def is_word_end(text, index):
    try:
        return index in text.ends_of_words
    except AttributeError:

        return False


def get_n_gram_at_i(text, n, i):
    if i < 0:
        return None
    gram = ""
    k = i
    while k - i < n:
        try:
            gram += text[k]
            k += 1
        except IndexError:
            return None
        if is_word_end(text, k - 1):
            stripped = text.stripped_part[text.ends_of_words[k-1]]
            j = 0
            while k - i < n and j < len(stripped):
                gram += stripped[j]
                k += 1
                j += 1
    return gram


def get_n_gram_at_i_v2(text, n, i):
    if i < 0 or i+n > len(text):
        return None
    gram = ""
    for k in range(i, i + n):
        if k == i or not is_word_end(text, k-1):
            gram += text[k]
        else:
            return None
    return gram


def calculate_n_gram_frequencies(text, n):
    frequencies_dict = {}
    current_gram = ""
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
            pass


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i


def subtract_ith_gram_from_frequency_change(decryption, n_gram_length, i, frequencies_change):
    gram = get_n_gram_at_i(decryption, n_gram_length, i)
    if not gram:
        return
    try:
        frequencies_change[gram] -= 1
    except KeyError:
        frequencies_change[gram] = -1


def add_ith_gram_to_frequency_change(decryption, n_gram_length, i, frequencies_change):
    gram = get_n_gram_at_i(decryption, n_gram_length, i)
    if not gram:
        return
    try:
        frequencies_change[gram] += 1
    except KeyError:
        frequencies_change[gram] = 1


def expected_value(log_frequencies, text_length):
    normalizer = 0
    expected = 0
    for i in log_frequencies:
        normalizer += exp(log_frequencies[i])
    for i in log_frequencies:
        expected += log_frequencies[i]*exp(log_frequencies)
    return (expected/normalizer)*text_length
