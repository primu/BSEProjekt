
class MNISTReader(object):
    _label_file_path = None
    _images_file_path = None

    def __init__(self, label_file_path, images_file_path):
        self._label_file_path = label_file_path
        self._images_file_path = images_file_path

    def get_next(self):
        with open(self._label_file_path, "rb") as labels, open(self._images_file_path, "rb") as images:
            label_buffer = 1
            image_buffer = [[0 for x in range(28)] for x in range(28)]
            current_image_number = 0

            labels.seek(4)
            number_of_images = int.from_bytes(labels.read(4), byteorder="big")

            images.seek(8)
            rows = int.from_bytes(images.read(4), byteorder="big")
            columns = int.from_bytes(images.read(4), byteorder="big")

            while True:
                current_image_number += 1
                print("Current image number: {}/{}".format(current_image_number, number_of_images))
                label_bytes = labels.read(1)
                if label_bytes == b'':
                    break
                label_buffer = int.from_bytes(label_bytes, byteorder="big")
                for row in range(rows):
                    for column in range(columns):
                        image_buffer[row][column] = int.from_bytes(images.read(1), byteorder="big")

                yield label_buffer, image_buffer
