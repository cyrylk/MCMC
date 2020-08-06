## @brief package containing alphabetic class definition
# and related "alphabetic" functions


## @brief class containing information about the alphabet used
class Alphabet:
    def __init__(self, alphabet_in_iterable):
        ## @brief alphabet used
        self.alphabet = list(alphabet_in_iterable)
        ## @brief mapping of letters to their positions
        self.letters_to_position = {self.alphabet[i]: i for i in range(len(self.alphabet))}
        ## @brief length of the alphabet
        self.length = len(self.alphabet)
        ## @brief number of different letters, than given one, in alphabet
        # (equiv number of shifts that will change a letter)
        self.max_shift_length = self.length - 1

    def __getitem__(self, key):
        return self.alphabet[key]

    def __contains__(self, item):
        return item in self.letters_to_position


## @brief class containing the input text stripped of non-alphabetic characters
# alongside with all the information needed to recreate the original text
class StrippedText:
    def __init__(self, text, alphabet):
        length = len(text)
        self.non_stripped_part = []
        self.stripped_part = []
        self.ends_of_words = {}
        end_of_word = 0
        word_number = 0
        stripped = ""
        for i in range(length):
            if text[i] in alphabet:
                self.non_stripped_part.append(text[i])
                if stripped:
                    self.stripped_part.append(stripped)
                    stripped = ""
                    self.ends_of_words[(end_of_word - 1)] = len(self.stripped_part) - 1
                    if end_of_word:
                        word_number += 1
                if i + 1 == length:
                    self.ends_of_words[end_of_word] = len(self.stripped_part)
                end_of_word += 1
            else:
                stripped += text[i]
                if i + 1 == length:
                    if stripped:
                        self.stripped_part.append(stripped)
                    self.ends_of_words[(end_of_word - 1)] = len(self.stripped_part) - 1

        self.stripped_part.append("")

    def __getitem__(self, key):
        return self.non_stripped_part[key]

    def __setitem__(self, key, value):
        self.non_stripped_part[key] = value

    def __len__(self, ):
        return len(self.non_stripped_part)

    def set_non_stripped_part(self, new_non_stripped_part):
        self.non_stripped_part = new_non_stripped_part

    def set_stripped_part(self, new_stripped_part):
        self.stripped_part = new_stripped_part

    def set_ends_of_words(self, new_ends_of_words):
        self.ends_of_words = new_ends_of_words

    def get_non_stripped_text(self):
        text = []
        if -1 in self.ends_of_words:
            text.append(self.stripped_part[self.ends_of_words[-1]])
        for i in range(len(self.non_stripped_part)):
            text.append(self.non_stripped_part[i])
            if i in self.ends_of_words:
                text.append(self.stripped_part[self.ends_of_words[i]])
        return "".join(text)


def alphabets_product(alphabet1, alphabet2):
    return {i + j: 0 for i in alphabet1 for j in alphabet2}


## @brief function generating a dictionary of all n-grams of given alphabetic
# to frequencies - initially all frequencies set to zero
def n_gram_dict(alphabet, n):
    result = [""]
    for i in range(n):
        result = alphabets_product(alphabet, result)
    return result

