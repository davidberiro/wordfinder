import string
import random
import json
def generator(numOfLetters):
    random_letters = [random.choice(string.letters).lower() for i in range(numOfLetters)]
    return json.dumps(random_letters)
