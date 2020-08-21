import unittest
import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.ciphers.autokey as autokey


class AutokeyTest(unittest.TestCase):
    def setUp(self):
        self.alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_encrypt_decrypt_single(self):
        self.assertEqual(autokey.encrypt_decrypt_single("A", 7, self.alphabet), "H")
        self.assertEqual(autokey.encrypt_decrypt_single("C", 25, self.alphabet), "B")
        self.assertEqual(autokey.encrypt_decrypt_single("_", 25, self.alphabet), "_")

    def test_encrypt_text(self):
        text = alphabetic.StrippedText("A B C D E", self.alphabet)
        self.assertEqual(autokey.encrypt_text(text, [1, 2], self.alphabet).get_non_stripped_text(),
                         "B D C E G")


if __name__ == '__main__':
    unittest.main()


