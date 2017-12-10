import string
import random
import json
import numpy

# this should probably be moved to app.py...
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03,\
'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15,\
'X': 0.15, 'Q': 0.10, 'Z': 0.25}
letters = []
freq = []
for key, value in englishLetterFreq.items():
 letters.append(key)
 freq.append(value)


freq = numpy.array(freq)
freq/=freq.sum();
###############################################################

def generator(numOfLetters):

    random_letters = [numpy.random.choice(letters, p=freq).lower() for i in range(numOfLetters)]
    return json.dumps(random_letters)

def id_generator(num):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num))
