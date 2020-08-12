import unittest
import decryption_problem.common.common as common
import decryption_problem.alphabetic.alphabetic as alphabetic


class MyTestCase(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.alphabet = alphabetic.Alphabet("ABCDEF")

    def test_calculate_frequencies(self):
        init_frequencies = common.calculate_n_gram_frequencies("ABCCCDE", 2, self.alphabet)
        self.assertEqual(init_frequencies["AB"], 1)
        self.assertEqual(init_frequencies["BC"], 1)
        self.assertEqual(init_frequencies["DE"], 1)
        self.assertEqual(init_frequencies["CC"], 2)
        self.assertEqual(init_frequencies["CD"], 1)


if __name__ == '__main__':
    unittest.main()
