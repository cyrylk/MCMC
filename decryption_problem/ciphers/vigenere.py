import decryption_problem.alphabetic.alphabetic as alphabetic


## @brief package containing functions for encrypting and decrypting texts with Vigenere cipher


## @brief function for encrypting/decrypting single letter in Vigenere cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabetic
# alphabetic - alphabetic used
def encrypt_decrypt_single(letter, shift, alphabet):
    if letter not in alphabet:
        return letter
    return alphabet[(alphabet.letters_to_position[letter] + shift) % alphabet.length]


def create_stripped_encryption_decryption(text, encryption_decryption, alphabet):
    result = alphabetic.StrippedText(encryption_decryption, alphabet)
    result.set_ends_of_words(text.ends_of_words)
    result.set_stripped_part(text.stripped_part)
    return result

## @brief function for coding/decoding text in given Vigenere cipher
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        current_key_ptr = (current_key_ptr + 1) % key_length
    if type(text) is alphabetic.StrippedText:
        return create_stripped_encryption_decryption(text, encrypted_decrypted, alphabet)
    return encrypted_decrypted


def update_decryption_by_key_index(decryption, changed_index, shift, key_length, alphabet):
    for index in range(changed_index, len(decryption), key_length):
        decryption[index] = encrypt_decrypt_single(decryption[index], shift, alphabet)


def reverse_key(key, alphabet):
    return [(-a) % alphabet.length for a in key]


def get_zero_mono_key():
    return 0


def get_all_mono_keys(alphabet):
    return list(range(alphabet.length))
