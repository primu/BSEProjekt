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
                "matrix": np.zeros(input_dimensions),
                "mean": np.zeros(input_dimensions)
            }

    def train(self, data):
        image_array = np.array(data)
        matrix, mean = self._memory["matrix"], self._memory["mean"]

        matrix = np.add(matrix, mean)
        matrix = np.add(matrix, image_array)
        mean = np.mean(matrix)
        matrix -= mean

        self._memory["matrix"] = matrix
        self._memory["mean"] = mean

        self._numbers_incorporated += 1

    def test(self, data=None):
        image_array = np.array(data)
        similar = 0
        width, height = self._dimensions
        for w in range(width):
            for h in range(height):
                similar += self._memory["matrix"][w][h] * image_array[w][h]

        return similar

    def get_memory(self):
        return self._memory


