import unittest
import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.ciphers.vigenere as vigenere


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_encrypt_decrypt_single(self):
        self.assertEqual(vigenere.encrypt_decrypt_single("A", 7, self.alphabet), "H")
        self.assertEqual(vigenere.encrypt_decrypt_single("C", 25, self.alphabet), "B")
        self.assertEqual(vigenere.encrypt_decrypt_single("_", 25, self.alphabet), "_")

    def test_encrypt_decrypt_text(self):
        self.assertEqual(vigenere.encrypt_decrypt_text("I LIKE TO FISH", [1, 2], self.alphabet),
                         list("J NJMF VP HJUI"))
        stripped_text = alphabetic.StrippedText("I LIKE TO FISH", self.alphabet)
        self.assertEqual(vigenere.encrypt_decrypt_text(stripped_text, [1, 2], self.alphabet),
                         list("JNJMFVPHJUI"))
        self.assertEqual(vigenere.encrypt_decrypt_text_v2("I LIKE TO FISH", [1, 2], self.alphabet),
                         list("J MKLG VP GKTJ"))

    def test_update_encryption_by_index(self):
        decryption = list("J MKLG VP GKTJ")
        vigenere.update_decryption_by_key_index(decryption, 1, -1, 2, self.alphabet)
        self.assertEqual(decryption, list("J MJLF UP GJTI"))

if __name__ == '__main__':
    unittest.main()
