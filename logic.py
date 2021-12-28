# psychic list
import random


class RandomPsychic(object):
    predict = int()
    history = []

    def get_predict(self):
        self.predict = random.randint(10, 99)

    def save_predict(self):
        self.history.append(self.predict)


class RangePsychic(RandomPsychic):
    predict = 9
    history = []

    def get_predict(self):
        if RangePsychic.predict < 99:
            self.predict += 1
            self.history.append(self.predict)
        else:
            self.predict = 10
            self.history.append(self.predict)


class Player(object):
    history = []
    psychics = [RandomPsychic(), RangePsychic()]
    proxy = [0, 0]

    def ask_psychics(self):
        for i in range(len(Player.psychics)):
            self.psychics[i].get_predict()

    def check_predict(self, digit):
        self.history.append(digit)
        for i in range(len(Player.psychics)):
            if self.psychics[i].predict == digit:
                self.proxy[i] += 1
            else:
                self.proxy[i] -= 1
            self.psychics[i].save_predict()
