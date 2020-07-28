

def generate_from_file(filename):
    f = open(filename, "r")
    lines = f.readlines()
    freqs = {}
    for i in lines:
        freqs[i.split()[0]] = int(i.split()[1])

    normalizer = 0
    for i in freqs:
        normalizer += freqs[i]
    for i in freqs:
        freqs[i] /= (normalizer / 10)

    return freqs
