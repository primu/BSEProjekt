import numpy as np


class SVD(object):

    @staticmethod
    def feature(memory, how_many_stays):
        u, s, v = np.linalg.svd(memory)
        S = np.diag([val if i < how_many_stays else 0 for i, val in enumerate(s)])
        feature = np.dot(S, v)

        for x in range(len(s) - how_many_stays):
            feature = np.delete(feature, -1, 0)

        return u, feature

    @staticmethod
    def transpose(array):
        return [list(i) for i in zip(*array)]


class DigitNeuronSVD(object):
    """
    Can be trained and then queried for results
    """

    _digit = None
    _dimensions = None
    _memory = None
    _temp = {}

    _numbers_incorporated = None

    _config = None

    def __init__(self, digit, input_dimensions, memory=None):
        """
        :param digit: Letter that this neuron will represent
        :return:
        """
        self._digit = digit

        self._dimensions = input_dimensions
        self._numbers_incorporated = 0

        if memory:
            self._memory = memory
            self._memory["dirty"] = True
        else:
            self._memory = {
                "dirty": True,
                "svd_first_of_s": 75,
                "svd_params": {
                    "feature": None,
                    "u": None
                },
                "data": []
            }

    def train(self, data):
        """
        Metoda trenowania neuronu, powinna aktualizowac pole _memory w obiekcie
        Wartosc pola jest zapisywana miedzy wywolaniami programu

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: None
        """
        data = [item for sublist in data for item in sublist]

        self._memory["data"].append(data)

        self._memory["dirty"] = True
        self._numbers_incorporated += 1

    def test(self, data=None):
        """
        Nalezy uzywa pamieci neuronu (zapisanej w self._memory)

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: skala podobienstwa
        """

        if self._memory["dirty"]:
            memory = SVD.transpose(self._memory["data"])
            u, feature = SVD.feature(memory, self._memory["svd_first_of_s"])
            self._memory["svd_params"]["u"] = u
            self._memory["svd_params"]["feature"] = feature
            self._memory["dirty"] = False

        data = [[item for sublist in data for item in sublist]]

        compare = np.dot(data, self._memory["svd_params"]["u"])
        for x in range(len(compare) - self._memory["svd_first_of_s"]):
            compare = np.delete(compare, -1, 1)

        return 100.0 - np.linalg.norm(compare.T - self._memory["svd_params"]["feature"])

    def get_memory(self):
        return self._memory


