class MNISTReader(object):
	_label_file_path = None
	_images_file_path = None

	def __init__(self, label_file_path, images_file_path):
		self._label_file_path = label_file_path
		self._images_file_path = images_file_path

	def _bytes2int(self, bytes):
		return int(bytes.encode("hex"), 16)

	def get_next(self):
		with open(self._label_file_path, "rb") as labels, open(self._images_file_path, "rb") as images:
			label_buffer = 1
			image_buffer = [[0 for x in range(28)] for x in range(28)]
			current_image_number = 0

			labels.seek(4)
			number_of_images = self._bytes2int(labels.read(4))

			images.seek(8)
			rows = self._bytes2int(images.read(4))
			columns = self._bytes2int(images.read(4))

			while True:
				current_image_number += 1
				print("Current image number: {}/{}".format(current_image_number, number_of_images))
				label_bytes = labels.read(1)
				if label_bytes == b'':
					break
				label_buffer = self._bytes2int(label_bytes)
				for row in range(rows):
					for column in range(columns):
						image_buffer[row][column] = self._bytes2int(images.read(1))

				yield label_buffer, image_buffer
