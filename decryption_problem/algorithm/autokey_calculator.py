import decryption_problem.ciphers.autokey as cipher
import decryption_problem.common.common as common


def get_frequency_change_fixed_key_length(old_key, new_key,
                                          n_gram_length, current_decryption, alphabet):
    change = common.find_change_in_key(old_key, new_key)
    frequencies_change = {}
    key_length = len(old_key)
    shift = new_key[change] - old_key[change]
    power = 1
    for j in range(change, len(current_decryption), key_length):
        for i in range(j - n_gram_length + 1, j + 1):
            common.subtract_ith_gram_from_frequency_change(current_decryption, n_gram_length, i, frequencies_change)

        current_decryption[j] = cipher.encrypt_decrypt_single(current_decryption[j], shift * power, alphabet)
        for i in range(j - n_gram_length + 1, j + 1):
            common.add_ith_gram_to_frequency_change(current_decryption, n_gram_length, i, frequencies_change)
        current_decryption[j] = cipher.encrypt_decrypt_single(current_decryption[j], -shift * power, alphabet)
        power *= (-1)

    return frequencies_change

