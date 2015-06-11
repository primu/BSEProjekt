import copy
import unittest

from fox import Matrix


class MyTestCase(unittest.TestCase):
    def test_matrix_roll(self):
        a = [[1, 2], [3, 4]]
        b = copy.deepcopy(a)
        b = Matrix.roll_up(b)

        self.assertEqual(b, [[3, 4], [1, 2]])

    def test_get_nth_submatrix(self):
        a = [[1, 2], [3, 4]]
        sub1 = Matrix.get_nth_submatrix(a, 0)
        self.assertEqual(sub1, [[1, 1], [4, 4]])
        sub2 = Matrix.get_nth_submatrix(a, 1)
        self.assertEqual(sub2, [[2, 2], [3, 3]])
        sub3 = Matrix.get_nth_submatrix(a, 2)
        self.assertEqual(sub1, sub3)

    def test_add(self):
        a = [[1, 2], [3, 4]]
        b = [[4, 3], [2, 1]]

        summary = Matrix.sum(a, b)
        self.assertEqual(summary, [[5, 5], [5, 5]])


if __name__ == '__main__':
    unittest.main()
