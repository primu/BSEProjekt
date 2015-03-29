import os
from conf import PROJECT_ROOT
from helpers import image_reader
from helpers.mnist_reader import MNISTReader
from mpi.mpi_digit_recognition import MPIDigitRecognition

rec = MPIDigitRecognition(os.path.join(PROJECT_ROOT, "conf.json"))
try:
    rec.run()
    if rec.is_main_node():
        reader = MNISTReader(os.path.join(PROJECT_ROOT, "algorithms/datasets/train/train-labels.idx1-ubyte"),
                             os.path.join(PROJECT_ROOT, "algorithms/datasets/train/train-images.idx3-ubyte"))

        for digit, digit_matrix in reader.get_next():
            rec.train(digit, digit_matrix)
        rec.persist_neurons_knowledge()
except KeyboardInterrupt:
    print("Nicely killing")
    rec.stop()