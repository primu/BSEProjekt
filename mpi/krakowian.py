import random
import itertools

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


class Krakowian(MPIWrapper):
    MATRIX1_TAG = 10
    MATRIX2_TAG = 20
    MATRIX3_TAG = 30

    _width = None
    _height = None

    _matrix1 = None
    _matrix2 = None


    def stop(self):
        pass

    def init_matrices(self):
        self._matrix1 = [[random.randint(0, 5) for _ in range(self._width)] for _ in range(self._height)]
        self._matrix2 = [[random.randint(0, 5) for _ in range(self._width)] for _ in range(self._height)]

    def main_node_task(self):
        self._width = int(input("Szerokosc krakowiana: "))
        self._height = int(input("Wysokosc krakowiana: "))
        self.init_matrices()

        print("Krakowian 1: " + str(self._matrix1))
        print("Krakowian 2: " + str(self._matrix2))

        # wyslanie macierzy 2
        for node in self._worker_nodes_ids:
            self._comm.send(self._matrix2, dest=node, tag=self.MATRIX2_TAG)

        results = [0] * self._width

        for node, column in zip(itertools.cycle(self._worker_nodes_ids), range(self._width)):
            # wysylanie kolumn macierzy 1
            self._comm.send({
                "column": Matrix.get_column(self._matrix1, column),
                "index": column
            }, dest=node, tag=self.MATRIX1_TAG)

        for node, column in zip(itertools.cycle(self._worker_nodes_ids), range(self._width)):
            subresult = self._comm.recv(source=node, tag=self.MATRIX3_TAG)
            results[subresult["column"]] = subresult["values"]

        # transpozycja
        results = Matrix.transpose(results)
        print("Cracovian result: " + str(results))


    def worker_node_task(self):
        self._matrix2 = Matrix.transpose(self._comm.recv(tag=self.MATRIX2_TAG))
        while True:
            column_data = self._comm.recv(tag=self.MATRIX1_TAG)
            column_length = len(column_data["column"])
            result = []
            subresult = 0
            index = 0
            for matrix1_value, matrix2_value in zip(itertools.cycle(column_data["column"]), Matrix.flatten(self._matrix2)):
                subresult += matrix1_value * matrix2_value
                index += 1
                if index == column_length:
                    index = 0
                    result.append(subresult)
                    subresult = 0

            self._comm.send({
                "column": column_data["index"],
                "values": result
            }, dest=self._main_node_id, tag=self.MATRIX3_TAG)


if __name__ == "__main__":
    krakowian = Krakowian()
    krakowian.run()