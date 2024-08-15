import sys

sys.path.append('../..')
import unittest
import numpy as np
from Utils.Math import calculate_distances, calculate_direction_cosines


class TestMath(unittest.TestCase):
    def test_calculate_direction_cosines(self):
        # 示例数据
        points1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        points2 = np.array([[2, 3, 4], [13, 14, 15], [16, 17, 18]])
        
        distances = np.sqrt(calculate_distances(points1, points2))

        x_consines, y_consines, z_consines = calculate_direction_cosines(points1, points2, distances)
        expected_x_consines = np.array([[0.57735027],
                                        [0.57735027],
                                        [0.57735027]])
        expected_y_consines = np.array([[0.57735027],
                                        [0.57735027],
                                        [0.57735027]])
        expected_z_consines = np.array([[0.57735027],
                                        [0.57735027],
                                        [0.57735027]])
        self.assertTrue(np.allclose(expected_x_consines, x_consines))
        self.assertTrue(np.allclose(expected_y_consines, y_consines))
        self.assertTrue(np.allclose(expected_z_consines, z_consines))


    def test_calculate_distances(self):
        # 示例数据
        points1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        points2 = np.array([[2, 3, 4], [13, 14, 15], [16, 17, 18]])

        distances = calculate_distances(points1, points2)
        expected_distances = np.array([[3], [243], [243]])

        np.testing.assert_allclose(distances, expected_distances)


if __name__ == '__main__':
    unittest.main()
