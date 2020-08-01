def calculate_zero_frequency(frequencies):
    return min(frequencies.values())


def get_n_gram_at_i(text, n, j, i):
    if j < 0 or j+n > len(text):
        return None
    gram = ""
    for k in range(j, j + n):
        gram += text[k]
    return gram


def calculate_frequencies(text, gram_length, alphabet):
    frequencies_dict = alphabet.n_gram_dict(alphabet, gram_length)
    current_gram = ""
    for i in range(len(text)):
        current_gram += text[i]
        if len(current_gram) > gram_length:
            current_gram = current_gram[1:]
        if len(current_gram) == gram_length:
            frequencies_dict[current_gram] += 1

    return frequencies_dict

def calculate_function(text, gram_length, distribution):
    prob = 1
    current_gram = ""
    for i in range(len(text)):
        current_gram += text[i]
        if len(current_gram) > gram_length:
            current_gram = current_gram[1:]
        if len(current_gram) == gram_length:
            prob *= distribution[current_gram]

    return prob


def calculate_candidate_function(old, frequencies_change, distribution):
    change = 1
    for i in frequencies_change:
        if i not in distribution or not distribution[i]:
            change *= MIN_FREQUENCY_FACTOR**frequencies_change[i]
        else:
            change *= distribution[i]**frequencies_change[i]
    return change*old


def calculate_candidate_change(frequencies_change, distribution):
    return calculate_candidate_function(1, frequencies_change, distribution)


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i


def get_frequencies_change(old_frequencies, new_frequencies):
    frequencies_change = {}
    for i in old_frequencies:
        if old_frequencies[i] != new_frequencies[i]:
            frequencies_change[i] = new_frequencies[i] - old_frequencies[i]
    return frequencies_change


def get_frequency_change_fixed(old_key, new_key, n, current_decryption, alphabet):
    change = find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    shift = new_key[change] - old_key[change]
    for i in range(change, len(current_decryption), key_length):
        for j in range(i - n + 1, i + 1):
            old_gram = find_n_gram_at_i(current_decryption, n, j, i, 0, alphabet)
            new_gram = find_n_gram_at_i(current_decryption, n, j, i, shift, alphabet)
            if old_gram and new_gram:
                try:
                    frequencies_change[old_gram] -= 1
                    frequencies_change[new_gram] += 1
                except KeyError:
                    frequencies_change[old_gram] = -1
                    frequencies_change[new_gram] = 1

    return frequencies_change



# wherever only alphabetic length is needed, make it this way
# set some constant arguments order
def update_decryption_fixed(old_key, new_key, current_decryption, alphabet):
    change = find_change_in_key(old_key, new_key)
    shift = (new_key[change] - old_key[change]) % alphabet.length
    for i in range(change, len(current_decryption), len(old_key)):
        current_decryption[i] = encrypt_decrypt_single(current_decryption[i], shift, alphabet)


def get_frequency_change_bounded(old_key, new_key, n, frequencies, text, current_decryption, alphabet):
    if len(old_key) == len(new_key):
        return get_frequency_change_fixed(old_key, new_key, n, current_decryption, alphabet)
    else:
        new_frequencies = calculate_frequencies(encrypt_decrypt_text(text, new_key, alphabet), n, alphabet)
        frequencies_change = get_frequencies_change(frequencies, new_frequencies)
        return frequencies_change


def update_decryption_bounded(new_key, old_key, text, current_decryption, alphabet):
    return


def update_frequency(frequency, frequency_change):
    for i in frequency_change:
        frequency[i] += frequency_change[i]