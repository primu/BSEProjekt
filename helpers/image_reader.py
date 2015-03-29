from PIL import Image
import numpy as np


class ImageConverter(object):

    @staticmethod
    def get_matrix(path, grayscale=True):
        image = Image.open(path)
        pixels, size = image.load(), image.size
        if not grayscale:
            return pixels, size
        new_pixels = []
        for x in range(size[0]):
            new_row = []
            for y in range(size[1]):
                pixel = pixels[x, y]
                avg = 255 - ((pixel[0] + pixel[1] + pixel[2]) / 3)
                new_row.append(avg)
            new_pixels.append(new_row)
        return new_pixels, size

    @staticmethod
    def to_image(matrix, path):
        height = len(matrix)
        width = len(matrix[0])
        matrix_rgb = np.zeros((width, height, 3), dtype=np.uint8)
        for x in range(height):
            for y in range(width):
                matrix_rgb[x, y] = (matrix[x][y], 0, 0)

        image = Image.fromarray(matrix_rgb, mode="L")
        image.save(path)
