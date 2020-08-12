import decryption_problem.ciphers.vigenere_extended as cipher
import decryption_problem.common.common as common


def get_frequency_change_fixed_key_length(old_key, new_key,
                                          n_gram_length, current_decryption, text, alphabet, coprimes):
    change = common.find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    for j in range(change, len(current_decryption), key_length):
        for i in range(j - n_gram_length + 1, j + 1):
            common.subtract_ith_gram_from_frequency_change(current_decryption, n_gram_length, i, frequencies_change)

        current_decryption[j] = cipher.encrypt_decrypt_single(text[j], new_key[change], alphabet, coprimes)
        for i in range(j - n_gram_length + 1, j + 1):
            common.add_ith_gram_to_frequency_change(current_decryption, n_gram_length, i, frequencies_change)
        current_decryption[j] = cipher.encrypt_decrypt_single(text[j], old_key[change], alphabet, coprimes)

    return frequencies_change
