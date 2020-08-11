import unittest


## @brief unit tests for Vigenere encryption and decryption_problem
class TestVigenereEncryptionDecryption(unittest.TestCase):

    def setUp(self):
        self.alphabet = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def patchRandint(self, min_value, max_value):
        return max_value // 2

    def test_single_letter_encrypt_decrypt(self):
        self.assertEqual(encrypt_decrypt_single("Z", 4, self.alphabet), "D")



    def test_text_encrypt_decrypt(self):
        self.assertEqual(encrypt_decrypt_text(list("YEARGREATYEAR"), [3, 2, 1, 0], self.alphabet), list("BGBRJTFAWAFAU"))

    def test_ith_fixed_neighbour(self):
        self.assertEqual(
            get_ith_neighbour_fixed([0, 1, 2, 3, 4, 5], 3 * self.alphabet.max_shift_length + 2, self.alphabet),
            [0, 1, 2, 6, 4, 5])

    def test_ith_bounded_neighbour(self):
        # deletion
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 4, 10, self.alphabet), [0, 1, 2, 3, 5])

        # insertion at the beginning
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 8, 10, self.alphabet), [2, 0, 1, 2, 3, 4, 5])

        # insertion in the middle
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 2 * self.alphabet.length + 7, 10, self.alphabet),
            [0, 1, 7, 2, 3, 4, 5])
        # insertion at the end
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 6 * self.alphabet.length + 1, 10, self.alphabet),
            [0, 1, 2, 3, 4, 5, 1])

        # substituting a letter
        self.assertEqual(get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 7 * self.alphabet.length +
                                                   2 * self.alphabet.max_shift_length + 23, 10, self.alphabet),
                         [0, 1, 0, 3, 4, 5])

        # boundary size
        self.assertEqual(
            get_ith_neighbour_bounded([0, 1, 2, 3, 4, 5], 6 + 5 * self.alphabet.max_shift_length + 2, 6, self.alphabet),
            [0, 1, 2, 3, 4, 8])

        # zero size
        self.assertEqual(get_ith_neighbour_bounded([], 6, 6, self.alphabet),
                         [6])

    def test_neighbours_number_fixed(self):
        self.assertEqual(get_neighbours_number_fixed([0, 1, 2, 3, 4, 5], self.alphabet),
                         6 * self.alphabet.max_shift_length)

    def test_neighbours_number_bounded(self):
        # middle size
        self.assertEqual(get_neighbours_number_bounded([0, 1, 2, 3, 4, 5], 10, self.alphabet),
                         6 * self.alphabet.max_shift_length +
                         6 + 7 * self.alphabet.length)
        # boundary size
        self.assertEqual(get_neighbours_number_bounded([0, 1, 2, 3, 4, 5], 6, self.alphabet),
                         6 * self.alphabet.max_shift_length + 6)

        # zero size
        self.assertEqual(get_neighbours_number_bounded([], 6, self.alphabet), self.alphabet.length)

    def test_candidate_fixed(self):
        with mock.mock.patch('random.randint', self.patchRandint):
            current_state = [0, 1, 2, 3, 4, 5]
            max_value = get_neighbours_number_fixed(current_state, self.alphabet) - 1
            self.assertEqual(get_candidate_fixed(current_state, self.alphabet),
                             get_ith_neighbour_fixed(current_state, max_value // 2, self.alphabet))

    def test_candidate_bounded(self):
        with mock.mock.patch('random.randint', self.patchRandint):
            current_state = [0, 1, 2, 3, 4, 5]
            max_value = get_neighbours_number_bounded(current_state, 10, self.alphabet) - 1
            self.assertEqual(get_candidate_bounded(current_state, 10, self.alphabet),
                             get_ith_neighbour_bounded(current_state, max_value // 2, 10, self.alphabet))



    def test_calculate_change_fixed(self):
        original_text = list("ABCD")
        self.assertEqual(get_frequency_change_fixed([0, 1], [0, 2], 2, encrypt_decrypt_text(original_text, [0,1], self.alphabet),
                                                    self.alphabet),
                         {"AC": -1, "AD": 1, "CC": -1, "DC": 1, "CE": -1, "CF": 1})

    # def test_calculate_change_bounded(self):
    #     text = "ABCD"
    #     frequencies = calculate_frequencies(encrypt_decrypt_text(text, [0, 1], self.alphabetic), 2, self.alphabetic)
    #     self.assertEqual(get_frequency_change_bounded([0, 1], [0, 1, 0], 2, frequencies, text),
    #                      {"CE": -1, "CD": 1})

    def test_update_frequency(self):
        frequency = {"AB": 1, "BC": 2, "CD": 0}
        frequency_change = {"AB": -1, "BC": -2, "CD": 3}
        update_frequency(frequency, frequency_change)
        self.assertEqual(frequency, {"AB": 0, "BC": 0, "CD": 3})

    def test_calculate_candidate_function(self):
        self.assertEqual(calculate_candidate_function(2, {"AB": 2, "CD": -1}, {"AB": 0.5, "CD": 0.25}), 2*4*0.25)


if __name__ == '__main__':
    unittest.main()
