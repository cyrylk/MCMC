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
        self.assertEqual(vigenere.encrypt_decrypt_text("MONTE CARLO", [1, 2], self.alphabet),
                         list("NQOVF DCSNP"))
        stripped_text = alphabetic.StrippedText("MONTE CARLO", self.alphabet)
        self.assertEqual(vigenere.encrypt_decrypt_text(stripped_text, [1, 2], self.alphabet).non_stripped_part,
                         list("NQOVFEBTMQ"))

    def test_update_encryption_by_index(self):
        decryption = list("J MKLG VP GKTJ")
        vigenere.update_decryption_by_key_index(decryption, 1, -1, 2, self.alphabet)
        self.assertEqual(decryption, list("J MJLF UP GJTI"))

if __name__ == '__main__':
    unittest.main()
