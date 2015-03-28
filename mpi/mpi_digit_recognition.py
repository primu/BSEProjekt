from Queue import Queue
import json
import random
import string
import threading
from time import sleep, time
# from uuid import uuid4 # jakims cudem to blokuje wykonanie w mpiexec.. dafuq
from mpi import image_reader
from mpi.mpi_wrapper import MPIWrapper
from algorithms.letter_recognition_simple.digit_neuron import DigitNeuron

class MPIDigitRecognition(MPIWrapper):

    _config = None

    _training_queue = None
    _query_queue = None

    _neuron = None

    _results = None

    # constants

    SPAWN_TAG = 10
    TRAINING_TAG = 20
    QUERYING_TAG = 30
    LOG_TAG = 40

    INPUT_TAG = 50
    OUTPUT_TAG = 60

    _QuitThread = object()

    def __init__(self, config_path):
        super(MPIDigitRecognition, self).__init__()
        self._load_config(config_path)

        self._training_queue = Queue()
        self._query_queue = Queue()

        self._results = {}

    def debug(self, text):
        if self._config["debug"]:
            print(text)

    def _load_config(self, config_path):
        with open(config_path) as conf_file:
            self._config = json.load(conf_file)

    def stop(self):
        self._query_queue.put(self._QuitThread)
        self._training_queue.put(self._QuitThread)

    def _node_for_digit(self, digit):
        return digit + 1

    def _main_node_logging_thread(self):
        while True:
            data = self._comm.recv(tag=MPIDigitRecognition.LOG_TAG)
            print(data)

    def _worker_node_log(self, data):
        if self._config["worker_debug"]:
            self._comm.send("Worker: {}".format(data), dest=self._main_node_id, tag=MPIDigitRecognition.LOG_TAG)

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
            self.debug("Got digit matrix, task id: {}".format(digit_matrix["id"]))
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
                self.debug("Got results from worker node: {}".format(json.dumps(data)))
                subresults.append(data)

            results = {"best_guess": "", "certainty": -1, "data": []}
            max_certainty = max([x["certainty"] for x in subresults if subresults]) if subresults else 0
            for result in subresults:
                certainty, neuron = (result["certainty"] / max_certainty) * 100.0, \
                                    result["neuron"]

                if certainty > results["certainty"]:
                    results["best_guess"] = neuron
                    results["certainty"] = certainty

                results["data"].append({
                    "neuron": neuron,
                    "certainty": certainty,
                })
            self._results[digit_matrix["id"]] = results

    def _worker_node_training_thread(self):
        while True:
            digit_matrix = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.TRAINING_TAG)
            self._neuron.train(digit_matrix)

    def _worker_node_querying_thread(self):
        while True:
            digit_matrix = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.QUERYING_TAG)
            result = self._neuron.test(digit_matrix)
            self._comm.send({
                "neuron": self._neuron._digit,
                "certainty": result
            }, dest=self._main_node_id, tag=MPIDigitRecognition.QUERYING_TAG)

    def main_node_task(self):
        for node, number in zip(self._worker_nodes_ids, range(0, 10)):
            self.debug("Starting node with id {}".format(node))
            self._comm.send({"digit": number}, dest=node, tag=MPIDigitRecognition.SPAWN_TAG)

        training_thread = threading.Thread(target=self._main_node_training_thread).start()
        querying_thread = threading.Thread(target=self._main_node_querying_thread).start()
        if self._config["worker_debug"]:
            logging_thread = threading.Thread(target=self._main_node_logging_thread).start()

        self.debug("Main node: threads ran")

    def worker_node_task(self):
        message = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.SPAWN_TAG)
        self._neuron = DigitNeuron(message["digit"], (28, 28))
        self._worker_node_log("Started: {}".format(message["digit"]))

        training_thread = threading.Thread(target=self._worker_node_training_thread).start()
        querying_thread = threading.Thread(target=self._worker_node_querying_thread).start()

        while True:
            sleep(0.1)

    def _wait_for_result(self, task_id):
        while self._results.get(task_id) is None:
            sleep(0.01)
        return True

    def query(self, digit_matrix):
        task_id = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(26))
        self._query_queue.put({
            "id": task_id,
            "data": digit_matrix
        })

        wait_thread = threading.Thread(target=self._wait_for_result, args=(task_id, ))
        wait_thread.start()
        wait_thread.join()
        return self._results.pop(task_id)

if __name__ == "__main__":
    print("Pre run")
    rec = MPIDigitRecognition("conf.json")
    try:
        print("Run")
        rec.run()
        print("After run")
        if rec.is_main_node():
            pixels, _ = image_reader.ImageConverter.get_matrix("../algorithms/letter_recognition_simple/data/other/2.jpg")
            print(rec.query(pixels))
    except KeyboardInterrupt:
        rec.stop()