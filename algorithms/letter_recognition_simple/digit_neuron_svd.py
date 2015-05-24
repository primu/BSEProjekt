import numpy as np


class SVD(object):

    @staticmethod
    def get_feature(memory, how_many_stays):
        u, s, v = np.linalg.svd(memory)
        S = np.diag([val if i <= how_many_stays else 0 for i, val in enumerate(s)][:how_many_stays])
        print(u.shape, s.shape, v.shape)
        for x in range(v.shape[0] - how_many_stays):
            v = np.delete(v, -1, 0)

        feature = np.dot(S, v)

        return u, feature

    @staticmethod
    def transpose(array):
        return [list(i) for i in zip(*array)]

    @staticmethod
    def flatten(data):
        return [item for sublist in data for item in sublist]

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
                "svd_first_of_s": 20,
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
        data = SVD.flatten(data)
        data = [1 if element > 0 else 0 for element in data]
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
            # memory = self._memory["data"]
            u, feature = SVD.get_feature(memory, self._memory["svd_first_of_s"])
            self._memory["svd_params"]["u"] = u
            self._memory["svd_params"]["feature"] = feature
            self._memory["dirty"] = False

        data = SVD.flatten(data)
        data = [1 if element > 0 else 0 for element in data]
        # data = SVD.transpose([data])

        vector_length = len(data)
        data_length = self._memory["svd_first_of_s"]# len(self._memory["data"])

        print(vector_length)
        print(data_length)


        compare = np.dot(data, self._memory["svd_params"]["u"])
        compare = np.repeat(compare, data_length, axis=0)
        compare = compare.reshape((vector_length, data_length))

        print(compare.shape)
        print(self._memory["svd_params"]["feature"].shape)
        distance = np.linalg.norm(compare[0] - self._memory["svd_params"]["feature"].T)
        # min_value = distance
        #
        # for i in range(1, vector_length):
        #     distance = np.linalg.norm(compare[i] - self._memory["svd_params"]["feature"])
        #     if min_value > distance:
        #         min_value = distance

        return abs(distance)

    def get_memory(self):
        return self._memory


