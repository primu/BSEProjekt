import json
from multiprocessing.pool import ThreadPool
import pickle
import sys

from digit_neuron_svd import DigitNeuronSVD
from helpers import image_reader
from helpers.utils import full_path_for, get_class


class DigitTrainer(object):
    _neurons = None
    _conf = None
    _all = None

    _reader = None

    def start_thread(self, number):
        print("Starting " + str(number))
        try:
            memory = pickle.load(open(full_path_for(self._conf["neurons"]["knowledge_path"]).format(number)))
        except Exception:
            print("Warning, no knowledge for " + str(number))
            memory = None

        return DigitNeuronSVD(number, tuple(self._conf["neurons"]["class"]["size"]), memory)

    def __init__(self, conf_file):
        with open(full_path_for(conf_file)) as f:
            self._conf = json.load(f)
        self._reader = get_class(self._conf["learn"]["reader"]["package"], self._conf["learn"]["reader"]["cls"])
        self._all = self._conf["neurons"]["charset"]
        p = ThreadPool(5)
        self._neurons = p.map(self.start_thread, self._all)


    def train(self, label_file_path, images_file_path, how_manu):
        # specjalny trainer ktory jest w stanie odczytywac z plikow MNIST
        reader = self._reader(label_file_path, images_file_path)
        processed = 0
        last_processed_char = 0
        for character, image in reader.get_next():
            self._neurons[self._all.index(character)].train(image)
            if processed == how_many:
                break
            if last_processed_char != character:
                last_processed_char = character
                print("New char", character)
            processed += 1


    def end_training(self):
        for index, neuron in enumerate(self._neurons):
            print("Dumping {}..".format(index))
            pickle.dump(neuron.get_memory(), open(full_path_for(self._conf["neurons"]["knowledge_path"].format(self._all[index])), mode="wb"))

    def test(self, label_file_path, images_file_path, how_many):
        reader = self._reader(label_file_path, images_file_path)
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
        for index, neuron in enumerate(self._neurons):
            print("Dumping {}..".format(index))
            neuron.dump_memory()


if __name__ == "__main__":
    dt = DigitTrainer(sys.argv[1])

    params = sys.argv[2:]

    # tu jest trenowanie ze specjalnego formatu dostarczonego przez MNIST - mozna nadpisac
    if "train" in params:
        try:
            how_many = int(params[-1])
        except ValueError:
            how_many = 9999999
        print("Train")
        dt.train(dt._conf["learn"]["train"]["labels_path"], dt._conf["learn"]["train"]["images_path"], how_many)

        # zapisanie wiedzy do pliku - wazne!!
        dt.end_training()

    if "test" in params:
        try:
            how_many = int(params[-1])
        except ValueError:
            how_many = 999999
        # testowanie przy uzyciu formatu MNIST - mozna nadpisac
        print("Test")
        dt.test(dt._conf["learn"]["test"]["labels_path"], dt._conf["learn"]["test"]["images_path"], how_many)
    # print(dt.test_file("data/other/2.jpg", "5"))
    # dt.dump_memory()

