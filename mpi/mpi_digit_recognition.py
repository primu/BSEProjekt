import importlib
import json
import random
import string
import threading
from time import sleep

from Queue import Queue


# from uuid import uuid4 # jakims cudem to blokuje wykonanie w mpiexec.. dafuq
import pickle
from helpers.path_for import full_path_for
from mpi.mpi_wrapper import MPIWrapper


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
    PERSISTING_TAG = 50

    _QuitThread = "quit"

    def __init__(self, config_path):
        super(MPIDigitRecognition, self).__init__()
        if self.is_main_node():
            self._load_config(config_path)

            self._training_queue = Queue()
            self._query_queue = Queue()

            self._results = {}

    def debug(self, text):
        """
        Prints text to stdout if "debug" varialbe in config file is true
        :param text: text to be debugged
        :return:
        """
        if self._config.get("debug"):
            print(text)

    def _load_config(self, config_path):
        """
        Load configs
        :param config_path: path to config file
        :return:
        """
        with open(config_path) as conf_file:
            self._config = json.load(conf_file)

    def _get_memory_for_neuron(self, neuron):
        file_path = full_path_for(self._config["neurons"].get("knowledge_path").format(neuron))
        try:
            return pickle.load(open(file_path, "rb"))
        except IOError:
            print("File not found: {}".format(file_path))
            return False

    def _save_memory_for_neuron(self, neuron, memory):
        file_path = full_path_for(self._config["neurons"].get("knowledge_path").format(neuron))
        pickle.dump(memory, open(file_path, "wb"))
        self.debug("Memory for {} saved to {}".format(neuron, file_path))

    def stop(self):
        """
        Stop all instances - main and workers
        :return:
        """
        if self.is_main_node():
            self._query_queue.put({"data": self._QuitThread, "id": "QUIT"})
            # todo: beautify
            for node in self._worker_nodes_ids:
                self.train(node - 1, self._QuitThread)

            self.train(self._QuitThread, self._QuitThread)

    def _node_for_digit(self, digit):
        """
        Return node id (rank) to which digit is mapped
        :param digit: digit to be mapped on node
        :return:
        """
        return digit + 1

    def _main_node_logging_thread(self):
        """
        Logging thread ran on main node, receiving data from worker nodes
        :return:
        """
        while True:
            data = self._comm.recv(tag=MPIDigitRecognition.LOG_TAG)
            print(data)

    def _worker_node_log(self, text):
        """
        Logging method on the worker node, forwards message to master
        :param text:
        :return:
        """
        if self._config.get("worker_debug"):
            self._comm.send("Worker: {}".format(text), dest=self._main_node_id, tag=MPIDigitRecognition.LOG_TAG)

    def _main_node_training_thread(self):
        """
        Training thread on main node, sends out the elements from training queue
        to appropriate worker node
        :return:
        """
        while True:
            data = self._training_queue.get(block=True)
            if data["digit"] == data["data"] == self._QuitThread:
                self.debug("Got kill signal, quitting..")
                break
            self._comm.send(data["data"],
                        dest=self._node_for_digit(data["digit"]),
                        tag=MPIDigitRecognition.TRAINING_TAG)

    def _main_node_querying_thread(self):
        """
        Querying thread on main node, sends out the element from querying queue
        to all workers nodes, receives the results, joins them and puts them in
        "results" dictionary in main node under the task "id" key.
        :return:
        """
        current_id = None
        while True:
            digit_matrix = self._query_queue.get(block=True)
            current_id = digit_matrix["id"]
            self.debug("Got digit matrix, task id: {}".format(digit_matrix["id"]))
            for node in self._worker_nodes_ids:
                self._comm.send(digit_matrix["data"],
                                dest=node,
                                tag=MPIDigitRecognition.QUERYING_TAG)

            if digit_matrix["data"] == MPIDigitRecognition._QuitThread:
                break

            subresults = []

            for node in self._worker_nodes_ids:
                data = self._comm.recv(source=node,
                                       tag=MPIDigitRecognition.QUERYING_TAG)
                data["certainty"] += 1000000000.0
                self.debug("Got results from worker node: {}".format(json.dumps(data)))
                subresults.append(data)

            results = {"best_guess": "", "certainty": -1, "data": []}
            max_certainty = max([x["certainty"] for x in subresults])

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
            self.debug(self._results)
        self._results[current_id] = None

    def _worker_node_training_thread(self):
        """
        Training thread on worker node, trains the underlying neuron with data send out by main node
        :return:
        """
        while True:
            digit_matrix = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.TRAINING_TAG)
            if digit_matrix == self._QuitThread:
                break
            self._neuron.train(digit_matrix)

    def _worker_node_querying_thread(self):
        """
        Querying thread on worker node, queries the underlying neuron for results
        :return:
        """
        while True:
            digit_matrix = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.QUERYING_TAG)
            if digit_matrix == self._QuitThread:
                break
            result = self._neuron.test(digit_matrix)
            self._comm.send({
                "neuron": self._neuron._digit,
                "certainty": result
            }, dest=self._main_node_id, tag=MPIDigitRecognition.QUERYING_TAG)

    def _worker_node_persisting_thread(self):
        while True:
            request = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.PERSISTING_TAG)
            if request == self._QuitThread:
                break
            self._comm.send(self._neuron.get_memory(), dest=self._main_node_id, tag=MPIDigitRecognition.PERSISTING_TAG)

    def main_node_task(self):
        """
        Main node main task, spawns training, querying threads and the logging thread for workers if
        set in config file to do so.
        :return:
        """
        if self._config["worker_debug"]:
            logging_thread = threading.Thread(target=self._main_node_logging_thread).start()
        for node, number in zip(self._worker_nodes_ids, range(0, 10)):
            self.debug("Starting node with id {}, memory".format(node))
            self._comm.send({
                "digit": number,
                "config": self._config,
                "memory": self._get_memory_for_neuron(number)
            }, dest=node, tag=MPIDigitRecognition.SPAWN_TAG)

        training_thread = threading.Thread(target=self._main_node_training_thread).start()
        querying_thread = threading.Thread(target=self._main_node_querying_thread).start()

        self.debug("Main node: threads ran")

    def worker_node_task(self):
        """
        Worker node main task, spawns the neuron given the digit from main node
        and starts training and querying threads
        :return:
        """
        message = self._comm.recv(source=self._main_node_id, tag=MPIDigitRecognition.SPAWN_TAG)
        self._config = message["config"]

        klass_object = self._config["neurons"]["class"]
        module = importlib.import_module(klass_object["package"])

        cls = getattr(module, klass_object["cls"])
        input_image_size = (klass_object["size"][0], klass_object["size"][1])

        self._neuron = cls(message["digit"], input_image_size, message["memory"])
        self._worker_node_log("Started: {}, size: {}".format(message["digit"], input_image_size))

        training_thread = threading.Thread(target=self._worker_node_training_thread).start()
        querying_thread = threading.Thread(target=self._worker_node_querying_thread).start()
        persisting_thread = threading.Thread(target=self._worker_node_persisting_thread).start()

    def _wait_for_result(self, task_id):
        """
        Waits for the result in results dictionary under given task_id
        :param task_id:
        :return:
        """
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

    def train(self, digit, digit_matrix):
        self._training_queue.put({
            "digit": digit,
            "data": digit_matrix
        })

    def persist_neurons_knowledge(self):
        for node, number in zip(self._worker_nodes_ids, range(0, 10)):
            self._comm.send(True, dest=node, tag=MPIDigitRecognition.PERSISTING_TAG)
            memory = self._comm.recv(source=node, tag=MPIDigitRecognition.PERSISTING_TAG)
            self._save_memory_for_neuron(number, memory)