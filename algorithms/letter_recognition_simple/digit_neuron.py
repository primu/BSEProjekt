import numpy as np


class DigitNeuron(object):
    """
    Can be trained and then queried for results
    """

    _digit = None
    _dimensions = None
    _memory = None

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
                "matrix": np.zeros(input_dimensions)
            }

    def train(self, data):
        """
        Metoda trenowania neuronu, powinna aktualizowac pole _memory w obiekcie
        Wartosc pola jest zapisywana miedzy wywolaniami programu

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: None
        """
        image_array = np.array(data)
        matrix = self._memory["matrix"]
        for position in np.ndenumerate(image_array):
            h = position[0][0]
            w = position[0][1]
            matrix[h][w] = (float(matrix[h][w]) + float(image_array[h][w])) / 2.0

        self._memory["matrix"] = matrix

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
                similar += similiar_subresult if similiar_subresult > 0 else (similiar_subresult / 4)

        return similar

    def get_memory(self):
        return self._memory


