## @brief package containing alphabetic class definition
# and related "alphabetic" functions


## @brief class containing information about the alphabetic used
class Alphabet:

    def __init__(self, alphabet_in_string):
        ## @brief alphabetic used
        self.alphabet = list(alphabet_in_string)
        ## @brief mapping of letters to their positions
        self.letters_to_position = {self.alphabet[i]: i for i in range(len(self.alphabet))}
        ## @brief length of the alphabetic
        self.length = len(self.alphabet)
        ## @brief number of different letters in alphabetic (equiv number of shifts that will change a letter)
        self.max_shift_length = self.length - 1

    def __getitem__(self, key):
        return self.alphabet[key]


def alphabets_product(alphabet1, alphabet2):
    return {i + j: 0 for i in alphabet1 for j in alphabet2}


## @brief function generating a dictionary of all n-grams of given alphabetic
# to frequencies - initially all frequencies set to zero
def n_gram_dict(alphabet, n):
    result = [""]
    for i in range(n):
        result = alphabets_product(alphabet, result)
    return result