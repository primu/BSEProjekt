import numpy as np

import json


def log(filename, data):
    with open(filename, "w") as file:
        file.write(json.dumps(data))


class SVD(object):

    @staticmethod
    def average_bucketize(memory, in_each_bucket=50, min_number_of_results=20):
        memory = np.array(memory, dtype=np.float)

        def avg_vector(single_vector, nums_of_concat):
            # single_vector /= float(nums_of_concat)
            max_value = max(single_vector)
            single_vector /= float(max_value)
            # single_vector[single_vector < 0.0] = 0.0

            return single_vector # np.array([1.0 if x > 0.0 else 0.0 for x in single_vector])

        result = []
        in_current_bucket = 0
        temp = None
        while len(result) < min_number_of_results:
            for vector in memory:
                if temp is None:
                    temp = vector
                else:
                    temp = np.add(temp, vector)
                in_current_bucket += 1
                if in_current_bucket == in_each_bucket:
                    result.append(avg_vector(temp, in_each_bucket))
                    temp = None
                    in_current_bucket = 0

        return result

    @staticmethod
    def get_feature(memory, how_many_stays):
        u, s, v = np.linalg.svd(memory)
        S = np.diag([val if i <= how_many_stays else 0 for i, val in enumerate(s)][:how_many_stays])
        print("Pre-process shapes", u.shape, s.shape, v.shape)
        for x in range(v.shape[0] - how_many_stays):
            v = np.delete(v, -1, 0)

        for x in range(u.shape[0] - how_many_stays):
            u = np.delete(u, -1, 1)

        feature = np.dot(S, v)
        print("Post-process shapes", u.shape, S.shape, v.shape)
        print("Feature shape", feature.shape)
        return u, feature

    @staticmethod
    def transpose(array):
        return [list(i) for i in zip(*array)]

    @staticmethod
    def flatten(data):
        return [item for sublist in data for item in sublist]

class DigitNeuronSVD(object):
    """
    Can be trained and then queried for results
    """

    _digit = None
    _dimensions = None
    _memory = None
    _temp = {}

    _numbers_incorporated = None

    _config = None

    def __init__(self, digit, input_dimensions, memory=None):
        """
        :param digit: Letter that this neuron will represent
        :return:
        """
        self._digit = digit

        self._dimensions = input_dimensions
        self._numbers_incorporated = 0

        self._in_each_bucket = 20
        self._svd_first_of_s = 10

        if memory:
            self._memory = memory
            self._memory["dirty"] = True
        else:
            self._memory = {
                "dirty": True,
                "svd_params": {
                    "feature": None,
                    "u": None
                },
                "data": []
            }

    def train(self, data):
        """
        Metoda trenowania neuronu, powinna aktualizowac pole _memory w obiekcie
        Wartosc pola jest zapisywana miedzy wywolaniami programu

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: None
        """
        data = SVD.flatten(data)
        # data = [1 if element > 0 else 0 for element in data]
        self._memory["data"].append(data)
        self._memory["dirty"] = True
        self._numbers_incorporated += 1

    def test(self, data=None):
        """
        Nalezy uzywa pamieci neuronu (zapisanej w self._memory)

        :param data: macierz z obrazkiem (o rozmiarach takich jak self._dimensions)
        :return: skala podobienstwa
        """

        if self._memory["dirty"]:
            print("Bucketize enter")
            memory = SVD.average_bucketize(self._memory["data"], self._in_each_bucket, self._svd_first_of_s)
            print("Bucketize end")
            memory = SVD.transpose(memory)
            print("Transpose end")
            u, feature = SVD.get_feature(memory, self._svd_first_of_s)
            print("Get feature end")
            self._memory["svd_params"]["u"] = u
            self._memory["svd_params"]["feature"] = feature
            self._memory["dirty"] = False
            print("Dirty end")

        data = SVD.flatten(data)
        max_value = max(data)
        data = np.array(data, dtype=np.float)
        data /= max_value
        # data = SVD.transpose([data])

        vector_length = len(data)
        data_length = self._svd_first_of_s # len(self._memory["data"])
        samples_length = self._memory["svd_params"]["feature"].shape[1]

        print("Vector length", vector_length)
        print("Data length", data_length)

        compare = np.dot(data, self._memory["svd_params"]["u"])

        #print("Compare post-dot", compare.shape)
        #compare = np.tile(compare, samples_length)
        #print("Compare pre-reshape", compare.shape)
        #compare = compare.reshape((data_length, samples_length))

        print(compare.shape)
        print(self._memory["svd_params"]["feature"].shape)

        log("compare", compare.tolist())
        log("feature", self._memory["svd_params"]["feature"].tolist())
        distance = np.linalg.norm(compare - self._memory["svd_params"]["feature"][:,0])
        min_value = distance

        for i in range(1, data_length):
            distance = np.linalg.norm(compare - self._memory["svd_params"]["feature"][:,i])
            if min_value > distance:
                min_value = distance

        return 100.0 - abs(min_value)

    def get_memory(self):
        return self._memory