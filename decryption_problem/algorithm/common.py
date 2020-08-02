import decryption_problem.alphabetic.alphabetic as alphabetic


def get_zero_frequency(frequencies):
    return min(frequencies.values())/2


def get_n_gram_at_i(text, n, i, alphabet):
    if i < 0 or i+n > len(text):
        return None
    gram = ""
    for k in range(i, i + n):
        if text[k] in alphabet.letters_to_position:
            gram += text[k]
        else:
            return None
    return gram


def calculate_n_gram_frequencies(text, n, alphabet):
    frequencies_dict = alphabetic.n_gram_dict(alphabet, n)
    current_gram = ""
    for i in range(len(text)):
        if text[i] not in alphabet.letters_to_position:
            current_gram = ""
            continue
        current_gram += text[i]
        if len(current_gram) > n:
            current_gram = current_gram[1:]
        if len(current_gram) == n:
            frequencies_dict[current_gram] += 1
    return frequencies_dict


def calculate_n_gram_function(frequencies, distribution):
    result = 1
    for i in frequencies:
        result *= distribution[i]**frequencies[i]
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
        result *= distribution[i]**frequencies_change[i]
    return result


def update_frequency(frequency, frequency_change):
    for i in frequency_change:
        frequency[i] += frequency_change[i]



