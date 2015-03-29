import os
from conf import PROJECT_ROOT
from helpers import image_reader
from helpers.mnist_reader import MNISTReader
from helpers.path_for import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition

rec = MPIDigitRecognition(full_path_for("conf.json"))
rec.run()
if rec.is_main_node():
    reader = MNISTReader(full_path_for("algorithms/datasets/train/train-labels.idx1-ubyte"),
                         full_path_for("algorithms/datasets/train/train-images.idx3-ubyte"))

    for digit, digit_matrix in reader.get_next():
        rec.train(digit, digit_matrix)
    rec.persist_neurons_knowledge()
    rec.stop()
