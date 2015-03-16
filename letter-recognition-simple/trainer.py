from digit_neuron import DigitNeuron
from mnist_reader import MNISTReader


class DigitTrainer(object):
    _neurons = None

    def __init__(self):
        self._neurons = []
        for x in range(10):
            self._neurons.append(DigitNeuron(x, (28, 28)))

    def train(self, label_file_path, images_file_path):
        reader = MNISTReader(label_file_path, images_file_path)
        for digit, image in reader.get_next():
            self._neurons[digit].train(image)

    def end_training(self):
        for neuron in self._neurons:
            neuron.end_training()

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


if __name__ == "__main__":
    dt = DigitTrainer()
    # dt.train("data/train/train-labels.idx1-ubyte", "data/train/train-images.idx3-ubyte")
    dt.end_training()
    dt.test("data/test/t10k-labels.idx1-ubyte", "data/test/t10k-images.idx3-ubyte")

