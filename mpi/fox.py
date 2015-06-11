import random
from time import sleep

import numpy as np

from mpi.mpi_wrapper import MPIWrapper


class Matrix():
    @staticmethod
    def get_column(matrix, column):
        return [x[column] for x in matrix]

    @staticmethod
    def get_row(matrix, row):
        return matrix[row]

    @staticmethod
    def transpose(matrix):
        return [list(x) for x in zip(*matrix)]

    @staticmethod
    def flatten(matrix):
        return [item for sublist in matrix for item in sublist]

    @staticmethod
    def get_nth_submatrix(matrix, nth):
        height = len(matrix)
        width = len(matrix[0])
        result = []

        for x in range(height):
            to_repeat = matrix[x][divmod(x + nth, width)[1]]
            result.append([to_repeat] * width)

        return result

    @staticmethod
    def roll_up(matrix):
        matrix.append(matrix.pop(0))
        return matrix

    @staticmethod
    def sum(matrix1, matrix2):
        matrix1 = np.array(matrix1)
        matrix2 = np.array(matrix2)

        return np.add(matrix1, matrix2).tolist()

    @staticmethod
    def dot(matrix1, matrix2):
        matrix1 = np.array(matrix1)
        matrix2 = np.array(matrix2)

        return (matrix1 * matrix2).tolist()



class Fox(MPIWrapper):

    SUM_TAG = 10
    END_TAG = 20


    def stop(self):
        pass

    def init_matrices(self):
        self._matrix1 = [[random.randint(0, 5) for _ in range(self._width)] for _ in range(self._height)]
        self._matrix2 = [[random.randint(0, 5) for _ in range(self._width)] for _ in range(self._height)]

    def main_node_task(self):
        self._width = int(input("Szerokosc macierzy: "))
        self._height = int(input("Wysokosc macierzy: "))
        self.init_matrices()

        self._matrix2 = Matrix.transpose(self._matrix2)

        print("Macierz 1: " + str(self._matrix1))
        print("Macierz 2: " + str(self._matrix2))

        sum = None

        for index in range(self._height):
            matrix1 = Matrix.get_nth_submatrix(self._matrix1, index)
            matrix2 = self._matrix2

            subsum = Matrix.dot(matrix1, matrix2)
            if sum is None:
                sum = subsum
            else:
                sum = Matrix.sum(sum, subsum)

            self._matrix2 = Matrix.roll_up(self._matrix2)

        print("Macierz 3: " + str(sum))


    def worker_node_task(self):
        while True:
            sleep(0.1)


if __name__ == "__main__":
    fox = Fox()
    fox.run()