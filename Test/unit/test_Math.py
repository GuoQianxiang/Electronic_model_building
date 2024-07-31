import sys

sys.path.append('../..')
import unittest
import numpy as np
from Utils.Math import calculate_distances, INT_SLAN_2D, calculate_potential, calculate_direction_cosines, copy_and_expand_matrix, update_matrix
from Model.Wires import Wire, Wires
from Model.Node import Node
from Model.Ground import Ground


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

    def test_calculate_potential_inductance(self):
        # 初始化节点数据
        node1 = Node('X01', 0, 0, 10.5)
        node2 = Node('X02', 1000, 0, 10.5)
        node3 = Node('X03', 0, -0.4, 10)
        node4 = Node('X04', 1000, -0.4, 10)
        node5 = Node('X05', 0, 0.1, 10)
        node6 = Node('X06', 1000, 0.1, 10)
        node7 = Node('X07', 0, 0.6, 10)
        node8 = Node('X08', 1000, 0.6, 10)

        # 初始化向量拟合参数
        frq = np.concatenate([
            np.arange(1, 91, 10),
            np.arange(100, 1000, 100),
            np.arange(1000, 10000, 1000),
            np.arange(10000, 100000, 10000),
            np.arange(100000, 1000000, 100000),
            np.arange(1000000, 10000000, 1000000),
            np.arange(10000000, 100000000, 10000000),
            np.arange(100000000, 1000000000, 100000000)
        ])
        VF = {'odc': 10,
            'frq': frq}

        # 根据节点连接成线段
        wire1 = Wire('Y01', node1, node2, 0, 0.005, 0, 0, 58000000, 1, 1, VF)
        wire2 = Wire('Y02', node3, node4, -0.4, 0.005, 0, 0, 58000000, 1, 1, VF)
        wire3 = Wire('Y03', node5, node6, 0.1, 0.005, 0, 0, 58000000, 1, 1, VF)
        wire4 = Wire('Y04', node7, node8, 0.6, 0.005, 0, 0, 58000000, 1, 1, VF)

        # 创建地面对象
        ground = Ground(1e-3, 1, 4, 'LSG', 'weak', 'isolational')

        # 创建线段集合
        wires = Wires()

        wires.add_air_wire(wire1)
        wires.add_air_wire(wire2)
        wires.add_ground_wire(wire3)
        wires.add_ground_wire(wire4)



        start_points = wires.get_start_points()
        end_points = wires.get_end_points()
        radii = wires.get_radii()
        lengths = wires.get_lengths()
        points_num = wires.count_distinct_points()

        L = INT_SLAN_2D(start_points, end_points, radii, start_points, end_points, radii, 2, 2)
  
        expected_inductance = np.array([[23798.45113262, 14094.68345806, 14549.89824057, 13697.6629857],
                                        [14094.68345806, 23798.45113262, 14589.09915526, 13203.80441899],
                                        [14549.89824057, 14589.09915526, 23798.45113262, 14589.09915526],
                                        [13697.6629857, 13203.80441899, 14589.09915526, 23798.45113262]])


        At = wires.get_bran_index()

        P = calculate_potential(start_points, end_points, lengths, radii, start_points, end_points, lengths, radii, At, points_num)

        expected_potential = np.array([[0.04482433, 0.00277257, 0.02541934, 0.00277003, 0.02632925, 0.00277055, 0.02462586, 0.00276947],  
                                       [0.00277257, 0.04482433, 0.00277003, 0.02541934, 0.00277055, 0.02632925, 0.00276947, 0.02462586],  
                                       [0.02541934, 0.00277003, 0.04482433, 0.00277257, 0.02640761, 0.00277059, 0.02363902, 0.00276859],  
                                       [0.00277003, 0.02541934, 0.00277257, 0.04482433, 0.00277059, 0.02640761, 0.00276859, 0.02363902],  
                                       [0.02632925, 0.00277055, 0.02640761, 0.00277059, 0.04482433, 0.00277257, 0.02640761, 0.00277059],  
                                       [0.00277055, 0.02632925, 0.00277059, 0.02640761, 0.00277257, 0.04482433, 0.00277059, 0.02640761],  
                                       [0.02462586, 0.00276947, 0.02363902, 0.00276859, 0.02640761, 0.00277059, 0.04482433, 0.00277257],  
                                       [0.00276947, 0.02462586, 0.00276859, 0.02363902, 0.00277059, 0.02640761, 0.00277257, 0.04482433]])
        self.assertTrue(np.allclose(L, expected_inductance))
        self.assertTrue(np.allclose(P, expected_potential))

    
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

if __name__ == '__main__':
    unittest.main()
