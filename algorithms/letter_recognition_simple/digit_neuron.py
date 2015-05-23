import numpy as np


class DigitNeuron(object):
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
        else:
            self._memory = {
                "matrix": np.zeros(input_dimensions),
                "mean": np.zeros(input_dimensions)
            }

    def svd_cut(self, data, how_many_stays):
        u, s, v = np.linalg.svd(data)
        new_s = [val if i < how_many_stays else 0.0 for i, val in enumerate(s)]
        S = np.diag(new_s)

        return np.dot(u, np.dot(S, v))

    def train(self, data):
        """
        Metoda trenowania neuronu, powinna aktualizowac pole _memory w obiekcie
        Wartosc pola jest zapisywana miedzy wywolaniami programu

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: None
        """
        image_array = np.array(data)
        matrix, mean = self._memory["matrix"], self._memory["mean"]

        matrix = np.add(matrix, mean)
        matrix = np.add(matrix, image_array)

        mean = np.mean(matrix)
        matrix = matrix - mean

        if self._numbers_incorporated % 1000 == 0:
            print(matrix)

        self._memory["matrix"] = matrix
        self._memory["mean"] = mean

        self._numbers_incorporated += 1

    def test(self, data=None):
        """
        Nalezy uzywa pamieci neuronu (zapisanej w self._memory)

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: skala podobienstwa
        """
        image_array = np.array(data)

        similar = 0
        width, height = self._dimensions
        for w in range(width):
            for h in range(height):
                similiar_subresult = self._memory["matrix"][h][w] * image_array[h][w]
                similar += int((similiar_subresult if similiar_subresult > 0 else (similiar_subresult * 50)) / 1000000)

        return similar

    def get_memory(self):
        return self._memory


