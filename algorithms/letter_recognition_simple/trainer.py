import os
import pickle

from digit_neuron import DigitNeuron
from helpers.mnist_reader import MNISTReader
from helpers import image_reader


class DigitTrainer(object):
    _neurons = None

    def __init__(self):
        self._neurons = []
        for x in range(10):
            # do listy neuronow dodajemy kolejne, wyspecjalizowane w rozpoznawaniu
            # liczb 0-9
            self._neurons.append(DigitNeuron(x, (28, 28)))

    def train(self, label_file_path, images_file_path):
        # specjalny trainer ktory jest w stanie odczytywac z plikow MNIST
        reader = MNISTReader(label_file_path, images_file_path)
        for digit, image in reader.get_next():
            self._neurons[digit].train(image)

    def end_training(self):
        for index, neuron in enumerate(self._neurons):
            pickle.dump(neuron.get_memory(), open(os.path.join("knowledge", "{}.data".format(index)), mode="wb"))

    def test(self, label_file_path, images_file_path):
        reader = MNISTReader(label_file_path, images_file_path)
        test_results = []
        for digit, image in reader.get_next():
            subresults = {"expected": str(digit),
                          "best_guess": {
                              "value": -999,
                              "neuron": ""
                          }}
            for i, neuron in enumerate(self._neurons):
                neuron_result = neuron.test(image)
                subresults[str(i)] = neuron_result
                if subresults["best_guess"]["value"] < neuron_result:
                    subresults["best_guess"]["value"] = neuron_result
                    subresults["best_guess"]["neuron"] = i
            test_results.append(subresults)

        correct_values = 0
        incorrect_values = 0
        # prosi sie o funkcyjne
        for result in test_results:
            if str(result["best_guess"]["neuron"]) == str(result["expected"]):
                correct_values += 1
            else:
                incorrect_values += 1

        print("Correct: {}, incorrect: {}, percent: {}".format(correct_values,
                                                                incorrect_values,
                                                                correct_values*100/(correct_values + incorrect_values)))

    def test_file(self, path, expected):
        pixels, size = image_reader.ImageConverter.get_matrix(path)
        result = {"expected": expected,
                          "best_guess": {
                              "value": -999,
                              "neuron": ""
                          }}
        for i, neuron in enumerate(self._neurons):
            neuron_result = neuron.test(pixels)
            result[str(i)] = neuron_result
            if result["best_guess"]["value"] < neuron_result:
                result["best_guess"]["value"] = neuron_result
                result["best_guess"]["neuron"] = i

        return result

    def dump_memory(self):
        for neuron in self._neurons:
            neuron.dump_memory()


if __name__ == "__main__":
    dt = DigitTrainer()
    dt.train("../datasets/train/train-labels.idx1-ubyte", "../datasets/train/train-images.idx3-ubyte")
    dt.end_training()
    dt.test("../datasets/test/t10k-labels.idx1-ubyte", "../datasets/test/t10k-images.idx3-ubyte")
    # print(dt.test_file("data/other/2.jpg", "5"))
    # dt.dump_memory()

