import decryption_problem.ciphers.autokey as autokey
import decryption_problem.common.common as common


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i


def subtract_ith_gram_from_frequency_change(decryption, n_gram_length, i, alphabet, frequencies_change):
    gram = common.get_n_gram_at_i(decryption, n_gram_length, i)
    if not gram:
        return
    try:
        frequencies_change[gram] -= 1
    except KeyError:
        frequencies_change[gram] = -1


def add_ith_gram_to_frequency_change(decryption, n_gram_length, i, alphabet, frequencies_change):
    gram = common.get_n_gram_at_i(decryption, n_gram_length, i)
    if not gram:
        return
    try:
        frequencies_change[gram] += 1
    except KeyError:
        frequencies_change[gram] = 1


def get_frequency_change_fixed_key_length(old_key, new_key,
                                          n_gram_length, current_decryption, alphabet):
    change = find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    shift = new_key[change] - old_key[change]
    power = 1
    for j in range(change, len(current_decryption), key_length):
        for i in range(j - n_gram_length + 1, j + 1):
            subtract_ith_gram_from_frequency_change(current_decryption, n_gram_length, i,
                                                    alphabet, frequencies_change)

        current_decryption[j] = autokey.encrypt_decrypt_single(current_decryption[j], shift*power, alphabet)
        for i in range(j - n_gram_length + 1, j + 1):
            add_ith_gram_to_frequency_change(current_decryption, n_gram_length, i, alphabet,
                                             frequencies_change)
        current_decryption[j] = autokey.encrypt_decrypt_single(current_decryption[j], -shift*power, alphabet)
        power *= (-1)

    return frequencies_change


# def get_frequency_change(current_frequencies, n_gram_length, new_key, text, alphabet):
#     new_frequencies = common.calculate_n_gram_frequencies(autokey.encrypt_decrypt_text(text, new_key, alphabet),
#                                                           n_gram_length, alphabet)
#     frequencies_change = common.get_frequencies_change(current_frequencies, new_frequencies)
#     return frequencies_change

