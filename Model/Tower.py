import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from Info import Info
from Wires import Wires
# from Lump import Circuit
from Ground import Ground
from Device import Device
from Node import MeasurementNode
import numpy as np


class Tower:
    def __init__(self, Info: Info, Wires: Wires, Lump, Ground: Ground, Device: Device, MeasurementNode: MeasurementNode):
        """
        初始化杆塔对象

        参数:
        Info (TowerInfo): 杆塔自描述信息对象
        Wires (Wires): 杆塔线段对象集合
        Lump (Circuit): 集中参数对象集合
        Ground (Ground): 杆塔地线对象集合
        Device (Device): 杆塔设备对象集合
        MeasurementNode (MeasurementNode): 杆塔测量节点对象集合

        无需传入的参数：
        nodesList (list): 杆塔节点名字列表
        nodesPositions (list): 杆塔节点坐标对列表
        incidence_matrix (numpy.ndarray, Num(wires) * Num(points)): 邻接矩阵
        """
        self.info = Info
        self.wires = Wires
        self.lump = Lump
        self.ground = Ground
        self.device = Device
        self.measurementNode = MeasurementNode
        self.nodesList = Wires.get_node_names()
        self.nodesPositions = Wires.get_node_coordinates()
        self.bransList = Wires.get_bran_coordinates()
        # 以下是参数矩阵，是Tower建模最终输出的参数
        # 邻接矩阵
        self.incidence_matrix = np.zeros((self.wires.count(), self.wires.count_distinct_points()))
        # 阻抗矩阵
        self.resistance_matrix = np.zeros((self.wires.count(), self.wires.count()))
        # 电感矩阵
        self.inductance_matrix = np.zeros((self.wires.count(), self.wires.count()))
        # 电位矩阵
        self.potential_matrix = np.zeros((self.wires.count_distinct_points(), self.wires.count_distinct_points()))


    def initialize_incidence_matrix(self):
        """
        initialize_incidence_matrix: calculate the incidence relationship of every wire.
        return: Num(wires) * Num(points) matrix.
                row represents the wire
                column represents the node
                element represents if this node is start point(-1) or end point(+1) for this wire.(neither is 0)
        """
        wire_index = 0
        all_nodes = self.wires.get_all_nodes()
        node_to_index = {node: node.id-1 for i, node in enumerate(all_nodes)}
        for wire_list in [self.wires.air_wires, self.wires.ground_wires, self.wires.a2g_wires, self.wires.short_wires, self.wires.tube_wires]:
            for wire in wire_list:
                start_node_index = node_to_index[wire.start_node]
                end_node_index = node_to_index[wire.end_node]
                self.incidence_matrix[wire_index][start_node_index] = -1
                self.incidence_matrix[wire_index][end_node_index] = 1
                wire_index += 1


    def initialize_resistance_matrix(self):
        """
        initialize_resistance_matrix: calculate the resistance of every wire.
        return: n*n diagonal matrix. diagonal elements are resistances of all wires.
        """
        # 1. calculate n*1 matrix for resistance of each wire
        # 2. np.diag(x) will take out the diagonal elements: if x.shape == n*n/n*1
        #    np.diag(x) will use x to create a diagonal matrix: if x.shape == 1*n
        #    so, we should flatten the result of self.wires.get_resistance()* self.wires.get_lengths()
        #    then, np.diag(flattened(x))
        self.resistance_matrix = np.diag((self.wires.get_resistance()* self.wires.get_lengths()).flatten())


    def initialize_inductance_matrix(self):
        """
        initialize_inductance_matrix: calculate the inductance of every wire.
        return: n*n diagonal matrix. diagonal elements are resistances of all wires.
        """
        self.inductance_matrix = np.diag((self.wires.get_inductance() * self.wires.get_lengths()).flatten())


    def initialize_potential_matrix(self):
        pass


    def update_inductance_matrix(self, L):
        self.inductance_matrix += L


    def update_potential_matrix(self, P):
        self.potential_matrix += P