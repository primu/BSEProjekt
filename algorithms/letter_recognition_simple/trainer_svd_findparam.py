import sys

from multiprocessing.pool import ThreadPool
import os
import pickle
from digit_neuron_svd import DigitNeuronSVD
from helpers.mnist_reader import MNISTReader
from helpers import image_reader
import json


def log(filename, data, mode="w"):
    with open(filename, mode) as file:
        file.write(json.dumps(data))


class DigitTrainer(object):
    _neurons = None

    def start_thread(self, number):
        print("Starting " + str(number))
        try:
            memory = pickle.load(open("knowledge/{}.data".format(number)))
        except Exception:
            print("Warning, no knowledge for " + str(number))
            memory = None

        return DigitNeuronSVD(number, (28, 28), memory)

    def __init__(self):
        p = ThreadPool(5)
        self._neurons = p.map(self.start_thread, list(range(10)))


    def train(self, label_file_path, images_file_path, how_manu):
        # specjalny trainer ktory jest w stanie odczytywac z plikow MNIST
        reader = MNISTReader(label_file_path, images_file_path)
        processed = 0
        for digit, image in reader.get_next():
            self._neurons[digit].train(image)
            if processed == how_many:
                break
            processed += 1


    def end_training(self):
        for index, neuron in enumerate(self._neurons):
            pickle.dump(neuron.get_memory(), open(os.path.join("knowledge", "{}.data".format(index)), mode="wb"))

    def test(self, label_file_path, images_file_path, how_many):

        for s in [1, 5, 10, 20, 40, 60, 80, 100]:
            for bucket in [3, 5, 10, 20, 30, 50]:

                reader = MNISTReader(label_file_path, images_file_path)
                test_results = []

                processed = 0

                for digit, image in reader.get_next():
                    if processed == how_many:
                        break
                    processed += 1

                    subresults = {"expected": str(digit),
                                  "best_guess": {
                                      "value": -999,
                                      "neuron": ""
                                  }}
                    print("Expected: " + str(digit))
                    for i, neuron in enumerate(self._neurons):
                        neuron._in_each_bucket = bucket
                        neuron._svd_first_of_s = s

                        neuron_result = neuron.test(image)
                        print("Neuron: " + str(i) + ", result: " + str(neuron_result))
                        print(neuron_result)
                        subresults[str(i)] = neuron_result
                        if subresults["best_guess"]["value"] < neuron_result:
                            subresults["best_guess"]["value"] = neuron_result
                            subresults["best_guess"]["neuron"] = i
                    test_results.append(subresults)
                    print("Guess: " + str(subresults["best_guess"]["neuron"]))

                correct_values = 0
                incorrect_values = 0
                # prosi sie o funkcyjne
                for result in test_results:
                    if str(result["best_guess"]["neuron"]) == str(result["expected"]):
                        correct_values += 1
                    else:
                        incorrect_values += 1

                percent = correct_values*100/(correct_values + incorrect_values)

                print("Correct: {}, incorrect: {}, percent: {}".format(correct_values,
                                                                        incorrect_values,
                                                                        percent))
                log("Log", "S: {}, bucket: {}, :{}\n".format(s, bucket, percent), "a")


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

    params = sys.argv[1:]

    # tu jest trenowanie ze specjalnego formatu dostarczonego przez MNIST - mozna nadpisac
    if "train" in params:
        try:
            how_many = int(params[-1])
        except ValueError:
            how_many = 9999999
        print("Train")
        dt.train("../datasets/train/train-labels.idx1-ubyte", "../datasets/train/train-images.idx3-ubyte", how_many)

        # zapisanie wiedzy do pliku - wazne!!
        dt.end_training()

    if "test" in params:
        try:
            how_many = int(params[-1])
        except ValueError:
            how_many = 999999
        # testowanie przy uzyciu formatu MNIST - mozna nadpisac
        print("Test")
        dt.test("../datasets/test/t10k-labels.idx1-ubyte", "../datasets/test/t10k-images.idx3-ubyte", how_many)
    # print(dt.test_file("data/other/2.jpg", "5"))
    # dt.dump_memory()

