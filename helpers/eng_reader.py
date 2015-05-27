import os
import string
from PIL import Image

import numpy as np

from helpers.image_processing import scale_to, crop2


class EnglishReader(object):
    _label_file_path = None
    _images_file_path = None

    _all = list(range(0, 10)) + list(string.ascii_uppercase)

    def __init__(self, label_file_path, images_file_path):
        self._label_file_path = label_file_path
        self._images_file_path = images_file_path

    def _bytes2int(self, bytes):
        return int(bytes.encode("hex"), 16)

    def get_next(self):
        i = 0
        for directory in os.listdir(self._images_file_path):
            for file in os.listdir(os.path.join(self._images_file_path, directory)):
                if not file.endswith("png"):
                    continue
                im = Image.open(os.path.join(self._images_file_path, directory, file)).convert("L")
                image = crop2(im)
                array = scale_to(image, 56, 56)

                label, data = self._all[i], np.array(array)

                yield label, data

            i += 1


if __name__ == "__main__":
    e = EnglishReader("", "../algorithms/datasets/char_test")
    for a, c in e.get_next():
        print(a, c)