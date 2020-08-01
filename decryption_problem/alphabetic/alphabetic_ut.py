import unittest
from decryption_problem.alphabetic import alphabetic as alphabetic


class AlphabetTest(unittest.TestCase):

    def test_alphabets_product(self):
        self.assertEqual(alphabetic.alphabets_product("AB", "C"), {"AC": 0, "BC": 0})

    def test_n_gram_dict(self):
        self.assertEqual(alphabetic.n_gram_dict("AB", 2), {"AA": 0, "AB": 0, "BA": 0, "BB": 0})


if __name__ == '__main__':
    unittest.main()
