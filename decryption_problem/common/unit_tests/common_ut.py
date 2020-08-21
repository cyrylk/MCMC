import unittest
import decryption_problem.common.common as common


class CommonTest(unittest.TestCase):

    def test_calculate_frequencies(self):
        init_frequencies = common.calculate_n_gram_frequencies("ABCCCDE", 2)
        self.assertEqual(init_frequencies["AB"], 1)
        self.assertEqual(init_frequencies["BC"], 1)
        self.assertEqual(init_frequencies["DE"], 1)
        self.assertEqual(init_frequencies["CC"], 2)
        self.assertEqual(init_frequencies["CD"], 1)


if __name__ == '__main__':
    unittest.main()
