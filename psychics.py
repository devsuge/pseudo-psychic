# psychic list
import random


class random_psychic(object):
    @staticmethod
    def predict():
        return random.randint(10, 99)


class range_psychic(random_psychic):
    @staticmethod
    def predict(last_digit):
        return last_digit + 1
