import string
import random
def generator(numOfLetters):
    random_letters = [random.choice(string.letters) for i in range(numOfLetters)]
    return random_letters
