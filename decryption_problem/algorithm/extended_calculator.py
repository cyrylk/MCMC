import decryption_problem.ciphers.vigenere_extended as extended
import decryption_problem.common.common as common


def find_change_in_key(old_key, new_key):
    for i in range(len(old_key)):
        if old_key[i] != new_key[i]:
            return i

# both extract to common
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


#two alphabets to be provided – extended and the one used for encryption/decryption
def get_frequency_change_fixed_key_length(old_key, new_key,
                                          n_gram_length, current_decryption, text, alphabet, coprimes):
    change = find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    for j in range(change, len(current_decryption), key_length):
        for i in range(j - n_gram_length + 1, j + 1):
            subtract_ith_gram_from_frequency_change(current_decryption, n_gram_length, i,
                                                    alphabet, frequencies_change)

        current_decryption[j] = extended.encrypt_decrypt_single(text[j], new_key[change], alphabet, coprimes)
        for i in range(j - n_gram_length + 1, j + 1):
            add_ith_gram_to_frequency_change(current_decryption, n_gram_length, i, alphabet,
                                             frequencies_change)
        current_decryption[j] = extended.encrypt_decrypt_single(text[j], old_key[change], alphabet, coprimes)

    return frequencies_change

#
# def get_frequency_change(current_frequencies, n_gram_length, new_key, text, alphabet):
#     new_frequencies = common.calculate_n_gram_frequencies(autokey.encrypt_decrypt_text(text, new_key, alphabet),
#                                                           n_gram_length, alphabet)
#     frequencies_change = common.get_frequencies_change(current_frequencies, new_frequencies)
#     return frequencies_change

