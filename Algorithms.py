from sklearn.naive_bayes import MultinomialNB
import numpy as np

'''

'''
class Algo:
    def __init__(self, data, classifications):
        self.data = data
        self.classifications = classifications
        self.classifier = None


class NB(Algo):
    def __init__(self, data, classifications):
        Algo.__init__(data, classifications)

    def train(self):
        self.classifier = MultinomialNB.fit(self.data, self.classifications)

    def predict(self, data):
        self.classifier.predict(data)



class NBCov(Algo):
    def __init__(self, data, classifications):
        Algo.__init__(data, classifications)

    def train(self):
        self.classifier = MultinomialNB.fit(self.data, self.classifications)

    def predict(self, data):
        self.classifier.predict(data)

