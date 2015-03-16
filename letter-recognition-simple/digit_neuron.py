import pickle
import numpy as np


class DigitNeuron(object):
    """
    Can be trained and then queried for results
    """

    _digit = None
    _dimensions = None
    _memory = None

    _numbers_incorporated = None

    _try_load_from_file = None
    _loaded_from_file = None

    def __init__(self, digit, input_dimensions, try_load_from_file=True):
        """

        :param digit: Letter that this neuron will represent
        :return:
        """
        self._digit = digit
        assert(isinstance(input_dimensions, tuple), "Not instance of tuple type")

        self._dimensions = input_dimensions
        self._memory = np.zeros(input_dimensions)
        self._numbers_incorporated = 0
        self._try_load_from_file = try_load_from_file

        if self._try_load_from_file:
            try:
                self._memory = pickle.load(open("tmp/{}.data".format(self._digit), "rb"))
                self._loaded_from_file = True
            except FileNotFoundError:
                pass

    def train(self, data):
        image_array = np.array(data)
        self._memory = np.add(self._memory, image_array)
        self._numbers_incorporated += 1

    def end_training(self):
        self._memory -= np.mean(self._memory)
        pickle.dump(self._memory, open("tmp/{}.data".format(self._digit), "wb"))


    def test(self, data=None):
        image_array = np.array(data)
        similar = 0
        width, height = self._dimensions
        for w in range(width):
            for h in range(height):
                similar += self._memory[w][h] * image_array[w][h]

        return similar


