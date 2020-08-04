import unittest
from decryption_problem.alphabetic import alphabetic as alphabetic


class AlphabetTest(unittest.TestCase):

    def test_alphabets_product(self):
        self.assertEqual(alphabetic.alphabets_product("AB", "C"), {"AC": 0, "BC": 0})

    def test_n_gram_dict(self):
        self.assertEqual(alphabetic.n_gram_dict("AB", 2), {"AA": 0, "AB": 0, "BA": 0, "BB": 0})

    def test_operators(self):
        self.assertEqual(alphabetic.Alphabet("ABC")[1], "B")
        self.assertTrue("B" in alphabetic.Alphabet("ABC"))
        self.assertFalse("D" in alphabetic.Alphabet("ABC"))

    def test_stripped_text_properties(self):
        stripped_text1 = alphabetic.StrippedText("LET US GO! IT IS TIME. ", alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertEqual(stripped_text1.ends_of_words, set([2, 4, 6, 8, 10, 14]))
        self.assertEqual(stripped_text1.stripped_part, [" ", " ", "! ", " ", " ", ". ", ""])
        self.assertEqual(stripped_text1.get_non_stripped_text(), "LET US GO! IT IS TIME. ")
        stripped_text2 = alphabetic.StrippedText("  LET US GO! IT IS TIME",
                                                 alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertEqual(stripped_text2.ends_of_words, set([-1, 2, 4, 6, 8, 10, 14]))
        self.assertEqual(stripped_text2.stripped_part, ["  ", " ", " ", "! ", " ", " ", ""])
        self.assertEqual(stripped_text2.get_non_stripped_text(), "  LET US GO! IT IS TIME")
        stripped_text2[0] = "A"
        self.assertEqual(stripped_text2[0], "A")



if __name__ == '__main__':
    unittest.main()
