import unittest
import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.ciphers.vigenere_extended as extended

class ExtendedTest(unittest.TestCase):
    def setUp(self):
        self.alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.coprimes = extended.get_coprimes(self.alphabet.length)

    def test_encrypt_decrypt_single(self):
        self.assertEqual(extended.encrypt_decrypt_single("A", (1, 7), self.alphabet, self.coprimes), "H")
        self.assertEqual(extended.encrypt_decrypt_single("B", (2, 7), self.alphabet, self.coprimes), "M")



if __name__ == '__main__':
    unittest.main()
