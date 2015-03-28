from mpi import image_reader
from mpi.mpi_digit_recognition import MPIDigitRecognition

rec = MPIDigitRecognition("conf.json")
try:
    rec.run()
    if rec.is_main_node():
        pixels, _ = image_reader.ImageConverter.get_matrix("../algorithms/letter_recognition_simple/data/other/2.jpg")
        print(rec.query(pixels))
except KeyboardInterrupt:
    print("Nicely killing")
    rec.stop()