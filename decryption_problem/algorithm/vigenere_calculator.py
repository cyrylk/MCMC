import decryption_problem.ciphers.vigenere as cipher
import decryption_problem.common.common as common


def get_frequency_change_fixed_key_length(old_key, new_key,
                                          n_gram_length, current_decryption, alphabet):
    change = common.find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    shift = new_key[change] - old_key[change]
    for i in range(change, len(current_decryption), key_length):
        for gram in common.get_n_grams_with_i(current_decryption, n_gram_length, i):
            common.subtract_gram_from_frequency_change(gram, frequencies_change)
        current_decryption[i] = cipher.encrypt_decrypt_single(current_decryption[i], shift, alphabet)
        for gram in common.get_n_grams_with_i(current_decryption, n_gram_length, i):
            common.add_gram_to_frequency_change(gram, frequencies_change)
        current_decryption[i] = cipher.encrypt_decrypt_single(current_decryption[i], -shift, alphabet)
    return frequencies_change
