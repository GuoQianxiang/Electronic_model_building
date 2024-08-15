import sys

sys.path.append('../..')

import unittest
import numpy as np
from Function.Calculators.Inductance import INT_SLAN_2D, calculate_potential
from Model.Wires import Wire, Wires
from Model.Node import Node
from Model.Ground import Ground


class TestCalculator(unittest.TestCase):
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