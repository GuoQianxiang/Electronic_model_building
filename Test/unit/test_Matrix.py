import sys

sys.path.append('../..')

import unittest
import numpy as np
from Utils.Matrix import copy_and_expand_matrix, update_matrix, update_and_sum_matrix


class TestMatrix(unittest.TestCase):
    def test_copy_and_expand_matrix(self):
        # 示例用法
        original_matrix = np.array([[1, 2, 3],
                                    [5, 6, 7],
                                    [8, 9, 10]])

        expanded_matrix = copy_and_expand_matrix(original_matrix, 3)
        expected_matrix = np.array([[0, 0, 0, 2, 2, 2, 3, 3, 3],
                                    [0, 0, 0, 2, 2, 2, 3, 3, 3],
                                    [0, 0, 0, 2, 2, 2, 3, 3, 3],
                                    [5, 5, 5, 0, 0, 0, 7, 7, 7],
                                    [5, 5, 5, 0, 0, 0, 7, 7, 7],
                                    [5, 5, 5, 0, 0, 0, 7, 7, 7],
                                    [8, 8, 8, 9, 9, 9, 0, 0, 0],
                                    [8, 8, 8, 9, 9, 9, 0, 0, 0],
                                    [8, 8, 8, 9, 9, 9, 0, 0, 0]])
        self.assertTrue(np.allclose(expanded_matrix, expected_matrix))


    def test_update_matrix(self):
        # 设置初始矩阵
        matrix = np.array([[1, 2, 3, 4], 
                           [5, 6, 7, 8],
                           [9, 10, 11, 12],
                           [13, 14, 15, 16]])

        # 设置子矩阵及要替换的行列索引
        submatrix = np.array([[100, 101], 
                              [102, 103]])
        indices = [1, 2]

        # 调用 update_matrix() 函数并检查结果
        updated_matrix = update_matrix(matrix, indices, submatrix)

        expected_matrix = np.array([[1, 2, 3, 4], 
                                    [5, 100, 101, 8],
                                    [9, 102, 103, 12],
                                    [13, 14, 15, 16]])

        self.assertTrue(np.allclose(updated_matrix, expected_matrix))
    

    def test_update_and_sum_matrix(self):
        # 创建一个 5x5 的示例矩阵
        matrix = np.array([[0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1],
                           [0, 1, 1, 1, 1]])

        # 执行矩阵操作
        result = update_and_sum_matrix(matrix)
        expected_result = np.array([[16, -4, -4, -4, -4],
                                    [-4, 1, 1, 1, 1],
                                    [-4, 1, 1, 1, 1],
                                    [-4, 1, 1, 1, 1],
                                    [-4, 1, 1, 1, 1]])
        self.assertTrue(np.allclose(result, expected_result))