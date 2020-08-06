import decryption_problem.alphabetic.alphabetic as alphabetic
from math import exp


def get_zero_frequency(frequencies):
    return min(frequencies.values())/2


def is_word_end(text, index):
    try:
        return index in text.ends_of_words
    except AttributeError:

        return False


def get_n_gram_at_i_v2(text, n, i, alphabet):
    if i < 0 or i+n > len(text):
        return None
    gram = ""
    for k in range(i, i + n):
        if (k == i or not is_word_end(text, k-1)):
            gram += text[k]
        else:
            return None
    return gram


#extended alphabet to be passed here
def get_n_gram_at_i(text, n, i, alphabet):
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


# extended alphabet to be passed here
def calculate_n_gram_frequencies(text, n, alphabet):
    frequencies_dict = alphabetic.n_gram_dict(alphabet, n)
    current_gram = ""
    for i in range(len(text)):
        # if text[i] not in alphabet:
        #     current_gram = ""
        #     continue
        current_gram += text[i]
        if len(current_gram) > n:
            current_gram = current_gram[1:]
        if len(current_gram) == n:
            try:
                frequencies_dict[current_gram] += 1
            except KeyError:
                pass
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
                        pass
    return frequencies_dict


def calculate_n_gram_function(frequencies, distribution):
    result = 1
    for i in frequencies:
        try:
            result *= distribution[i]**frequencies[i]
        except KeyError:
            pass
    return result


def calculate_log_n_gram_function(frequencies, log_distribution):
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


def calculate_function_change(frequencies_change, distribution):
    result = 1
    for i in frequencies_change:
        try:
            result *= distribution[i]**frequencies_change[i]
        except KeyError:
            pass
    return result


def calculate_log_function_change(frequencies_change, log_distribution):
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


def expected_value(log_frequencies, text_length):
    normalizer = 0
    expected = 0
    for i in log_frequencies:
        normalizer += exp(log_frequencies[i])

    for i in log_frequencies:
        expected += log_frequencies[i]*exp(log_frequencies)

    return (expected/normalizer)*text_length






