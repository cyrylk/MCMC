## @brief package containing functions for encrypting and decrypting texts with Vigenere cipher


## @brief function for encrypting/decrypting single letter in Vigenere cipher
# @param letter – letter to be encrypted/decrypted
# @param shift – how many places letter is to be shifted in the alphabetic
# alphabetic - alphabetic used
def encrypt_decrypt_single(letter, shift, alphabet):
    if letter not in alphabet.letters_to_position:
        return letter
    return alphabet[(alphabet.letters_to_position[letter] + shift) % alphabet.length]


## @brief function for coding/decoding text in given Vigenere cipher
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        if text[index] in alphabet.letters_to_position:
            encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
            current_key_ptr = (current_key_ptr + 1) % key_length
        else:
            encrypted_decrypted.append(text[index])
    return encrypted_decrypted


## @brief function for coding/decoding text in given Vigenere cipher version 2
# key is now aligned with non-alphabetic characters as well
# @param text – text to be coded/decoded
# @param code - code used for coding/decoding
# alphabetic - alphabetic used
def encrypt_decrypt_text_v2(text, shift_key, alphabet):
    key_length = len(shift_key)
    current_key_ptr = 0
    encrypted_decrypted = []
    for index in range(len(text)):
        if text[index] in alphabet.letters_to_position:
            encrypted_decrypted.append(encrypt_decrypt_single(text[index], shift_key[current_key_ptr], alphabet))
        else:
            encrypted_decrypted.append(text[index])
        current_key_ptr = (current_key_ptr + 1) % key_length
    return encrypted_decrypted


def update_decryption_by_key_index(decryption, changed_index, shift, key_length, alphabet):
    for index in range(changed_index, len(decryption), key_length):
        decryption[index] = encrypt_decrypt_single(decryption[index], shift, alphabet)
