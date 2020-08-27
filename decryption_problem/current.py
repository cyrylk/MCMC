import decryption_problem.alphabetic.alphabetic as alphabetic
import decryption_problem.ciphers.vigenere as vigenere
import decryption_problem.ciphers.autokey as autokey
import decryption_problem.ciphers.vigenere_extended as extended
from math import log

#
# alphabet = alphabetic.Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# print((extended.encrypt_decrypt_text(alphabetic.StrippedText("MONTE CARLO MARKOV CHAINZ", alphabet), [(0,1),(1,2)], alphabet,
#                                      extended.get_coprimes(alphabet.length)))
#       .get_non_stripped_text())
#
# print([alphabet.letters_to_position[l] if l in alphabet.letters_to_position else l
#        for l in "BCMONTECARLOMARKOVCHAI"])

def efficiency_to_latex_table(filee):
    print("\\begin{center}\\begin{tabular}{")
    print("|c|c|c|}")
    print("\\hline &\\multicolumn{2}{|c|}{SKUTECZNOŚĆ} \\\\ ")
    print("\\hline DŁUGOŚĆ KLUCZA & METODA MONOGRAMOWA & METODA BIGRAMOWA\\\\ \\hline")
    f = open(filee, "r")
    lines = f.readlines()
    for t in range(0, len(lines), 3):
        string_to_print = lines[t] + " & "
        string_to_print += str(float(lines[t+1].split(":")[1]))[:4] + " & "
        string_to_print += str(float(lines[t+2].split(":")[1]))[:4]
        string_to_print += "\\\\ \\hline"
        print(string_to_print)
    print("\\end{tabular}\\end{center}")
    f.close()

# efficiency_to_latex_table("./testing_and_results/efficiency_non_vigenere_stripped814.txt")

# for i in range(778688000):
# 	if not i%10000:
# 		print(i)
# import wikipedia
# #print(wikipedia.summary("Mathematics"))
# #wikipedia.search("Mathematics")
# print(wikipedia.page("Ice_hockey").content)

for i in range(50, 650, 50):
    print (26*(i * log(i)) + 10*i)