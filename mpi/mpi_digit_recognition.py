from Queue import Queue
import json
import threading
from time import sleep
from mpi.mpi_wrapper import MPIWrapper
from algorithms.letter_recognition_simple.digit_neuron import DigitNeuron


class MPIDigitRecognition(MPIWrapper):
    _config = None

    _training_queue = None
    _query_queue = None

    _neuron = None

    # constants

    SPAWN_TAG = 10
    TRAINING_TAG = 20
    QUERYING_TAG = 30

    INPUT_TAG = 50
    OUTPUT_TAG = 60

    _QuitThread = object()

    def __init__(self, config_path):
        super(MPIDigitRecognition, self).__init__()
        self._load_config(config_path)

        self._training_queue = Queue()
        self._query_queue = Queue()

    def _load_config(self, config_path):
        with open(config_path) as conf_file:
            self._config = json.load(conf_file)

    def _node_for_digit(self, digit):
        return digit + 1

    def _main_node_training_thread(self):
        while True:
            digit_matrix = self._training_queue.get(block=True)
            if digit_matrix is MPIDigitRecognition._QuitThread:
                break
            self._comm.send(digit_matrix["data"],
                            dest=self._node_for_digit(digit_matrix["digit"]),
                            tag=MPIDigitRecognition.TRAINING_TAG)

    def _main_node_querying_thread(self):
        while True:
            digit_matrix = self._query_queue.get(block=True)
            if digit_matrix is MPIDigitRecognition._QuitThread:
                break
            for node in self._worker_nodes_ids:
                self._comm.send(digit_matrix["data"],
                                dest=node,
                                tag=MPIDigitRecognition.QUERYING_TAG)
            subresults = []

            for node in self._worker_nodes_ids:
                data = self._comm.recv(source=node,
                                       tag=MPIDigitRecognition.QUERYING_TAG)
                subresults.append(data)

            results = {"best_guess": "", "certainty": -1, "data": []}
            max_certainty = max([x["result"] for x in subresults])
            for result in subresults:
                recognized, certainty, neuron = result["recognized"], \
                                                (result["certainty"] / max_certainty) * 100.0, \
                                                result["neuron"]

                if certainty > results["best_guess"]:
                    pass
                    # todo: dokonczyc

    def main_node_task(self):
        for node, number in zip(self._worker_nodes_ids, range(0, 10)):
            self._comm.send({"digit": number}, dest=node, tag=MPIDigitRecognition.SPAWN_TAG)

        training_thread = threading.Thread(target=self._main_node_training_thread).start()
        querying_thread = threading.Thread(target=self._main_node_querying_thread).start()

        # todo: usunac
        while not self._comm.Iprobe(tag=MPIDigitRecognition.SPAWN_TAG):
            sleep(1)
            print("Waiting")
        msg = self._comm.recv(tag=MPIDigitRecognition.SPAWN_TAG)
        print(msg)

    def worker_node_task(self):
        message = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.SPAWN_TAG)
        self._neuron = DigitNeuron(message["digit"], (28, 28))
        self._comm.send(message["digit"], dest=self._main_node_id, tag=MPIDigitRecognition.SPAWN_TAG)


if __name__ == "__main__":
    rec = MPIDigitRecognition("conf.json")
    rec.run()