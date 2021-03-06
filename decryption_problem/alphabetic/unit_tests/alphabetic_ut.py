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
        stripped_text1 = alphabetic.StrippedText("LET US GO! IT IS TIME. ",
                                                 alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertEqual(stripped_text1.ends_of_words, {2: 0, 4: 1, 6: 2, 8: 3, 10: 4, 14: 5})
        self.assertEqual(stripped_text1.stripped_part, [" ", " ", "! ", " ", " ", ". ", ""])
        self.assertEqual(stripped_text1.get_non_stripped_text(), "LET US GO! IT IS TIME. ")
        self.assertEqual(stripped_text1.positions["L"], set([0]))
        self.assertEqual(stripped_text1.positions["E"], set([1, 14]))
        stripped_text2 = alphabetic.StrippedText("  LET US GO! IT IS TIME",
                                                 alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertEqual(stripped_text2.ends_of_words, {-1: 0, 2: 1, 4: 2, 6: 3, 8: 4, 10: 5, 14: 6})
        self.assertEqual(stripped_text2.stripped_part, ["  ", " ", " ", "! ", " ", " ", ""])
        self.assertEqual(stripped_text2.get_non_stripped_text(), "  LET US GO! IT IS TIME")
        stripped_text2[3] = "F"
        self.assertEqual(stripped_text2[3], "F")
        self.assertEqual(stripped_text2.positions["F"], set([3]))



if __name__ == '__main__':
    unittest.main()

