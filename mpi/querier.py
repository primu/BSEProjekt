import os
import sys
from conf import PROJECT_ROOT
from helpers import image_reader
from helpers.mnist_reader import MNISTReader
from helpers.path_for import full_path_for
from mpi.mpi_digit_recognition import MPIDigitRecognition

rec = MPIDigitRecognition(full_path_for("conf.json"))
rec.run()
if rec.is_main_node():
    for filename in sys.argv[1:]:
        array, size = image_reader.ImageConverter.get_matrix(filename)
        print("Result for {}".format(filename))
        print(rec.query(array))
    rec.stop()
