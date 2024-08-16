import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from Info import Info
from Wires import Wires, TubeWire
from Ground import Ground
from Device import Device
from Node import MeasurementNode
import numpy as np
from scipy.linalg import block_diag
from Utils.Matrix import expand_matrix, copy_and_expand_matrix, update_matrix, update_and_sum_matrix


class Tower:
    def __init__(self, Info: Info, Wires: Wires, tubeWire: TubeWire, Lump, Ground: Ground, Device: Device,
                 MeasurementNode: MeasurementNode):
        """
        初始化杆塔对象

        参数:
        info (TowerInfo): 杆塔自描述信息对象
        wires (Wires): 杆塔线段对象集合
        tubeWire (TubeWire): 管状线段(杆塔中的管状线段唯一, 此处留存初始未切分的管状线段, 方便后续使用, 切分后的多个管状线存储于wires中)
        lump (Circuit): 集中参数对象集合
        ground (Ground): 杆塔地线对象集合
        device (Device): 杆塔设备对象集合
        measurementNode (MeasurementNode): 杆塔测量节点对象集合

        无需传入的参数：
        nodesList (list): 杆塔节点名字列表
        nodesPositions (list): 杆塔节点坐标对列表
        incidence_matrix (numpy.ndarray, Num(wires) * Num(points)): 邻接矩阵
        resistance_matrix (numpy.ndarray, Num(wires) * Num(wires)): 阻抗矩阵
        inductance_matrix (numpy.ndarray, Num(wires) * Num(wires)): 电感矩阵
        potential_matrix (numpy.ndarray, Num(points) * Num(points)): 电位矩阵
        capacitance_matrix (numpy.ndarray, Num(points) * Num(points)): 电容矩阵
        """
        self.info = Info
        self.wires = Wires
        self.tubeWire = tubeWire
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
        self.resistance_matrix = np.zeros((self.wires.count_airWires() + self.wires.count_gndWires(),
                                           self.wires.count_airWires() + self.wires.count_gndWires()))
        # 电感矩阵
        self.inductance_matrix = np.zeros((self.wires.count_airWires() + self.wires.count_gndWires(),
                                           self.wires.count_airWires() + self.wires.count_gndWires()))
        # 电位矩阵
        self.potential_matrix = np.zeros((self.wires.count_distinct_airPoints() + self.wires.count_distinct_gndPoints(),
                                          self.wires.count_distinct_airPoints() + self.wires.count_distinct_gndPoints()))
        # 电容矩阵
        self.capacitance_matrix = np.zeros((self.wires.count_distinct_points(), self.wires.count_distinct_points()))


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
        node_to_index = {node: i for i, node in enumerate(all_nodes)}
        for wire_list in [self.wires.air_wires, self.wires.ground_wires]:
            for wire in wire_list:
                start_node_index = node_to_index[wire.start_node]
                end_node_index = node_to_index[wire.end_node]
                self.incidence_matrix[wire_index][start_node_index] = -1
                self.incidence_matrix[wire_index][end_node_index] = 1
                wire_index += 1
        for tube_wire in self.wires.tube_wires:
            for core_wire in tube_wire.core_wires:
                start_node_index = node_to_index[core_wire.start_node]
                end_node_index = node_to_index[core_wire.end_node]
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
        self.resistance_matrix = np.diag((self.wires.get_resistance() * self.wires.get_lengths()).flatten())

    def initialize_inductance_matrix(self):
        """
        initialize_inductance_matrix: calculate the inductance of every wire.
        return: n*n diagonal matrix. diagonal elements are resistances of all wires.
        """
        self.inductance_matrix = np.diag((self.wires.get_inductance() * self.wires.get_lengths()).flatten())

    def initialize_potential_matrix(self):
        pass

    def initialize_capacitance_matrix(self):
        pass

    def add_inductance_matrix(self, L):
        self.inductance_matrix += L

    def add_potential_matrix(self, P):
        self.potential_matrix += P

    def expand_inductance_matrix(self):
        # 通过TubeWire的表皮与其他线段的互感，扩展复制代替为芯线与其他线段的互感，因为芯线和表皮实际上在一个位置
        for i in range(len(self.wires.tube_wires)):
            inner_num = self.wires.tube_wires[i].inner_num
            sheath_index = i + len(self.wires.air_wires) - len(self.wires.tube_wires)
            end_index = len(self.wires.air_wires) + len(self.wires.ground_wires)
            self.inductance_matrix = expand_matrix(self.inductance_matrix, sheath_index, end_index, inner_num)

    def update_inductance_matrix_by_coreWires(self):
        # 获取内部芯线的数量
        inner_num = self.wires.tube_wires[0].inner_num
        # 获取矩阵中表皮开始的索引和结束的索引
        sheath_start_index = len(self.wires.air_wires) - len(self.wires.tube_wires)
        sheath_end_index = len(self.wires.air_wires)
        # 获取空气和地面支路的结束位置
        end_index = len(self.wires.air_wires) + len(self.wires.ground_wires)
        # 单独获取表皮的电感矩阵
        sheath_inductance_matrix = self.inductance_matrix[sheath_start_index:sheath_end_index,
                                   sheath_start_index:sheath_end_index]
        self.inductance_matrix[end_index:, end_index:] = copy_and_expand_matrix(sheath_inductance_matrix, inner_num)
        return sheath_inductance_matrix

    def update_inductance_matrix_by_tubeWires(self, sheath_inductance_matrix, Lin, Lx):
        # 获取第一个管状线段的表皮和芯线在矩阵中的索引
        index = self.wires.get_tubeWires_start_index()
        # 获取索引增量，保证下面循环过程中，index+increment就是下一条管状线段的表皮和芯线的索引
        increment = self.wires.get_tubeWires_index_increment()

        L0 = Lin.copy()
        L0[0, 0] = 0
        for i in range(len(self.wires.tube_wires)):
            Lss = Lin[0, 0] + sheath_inductance_matrix[i, i]
            # L0+Lx+Lss的最终结果 更新到表皮和芯线的自感和互感位置上去
            self.inductance_matrix = update_matrix(self.inductance_matrix, index, L0 + Lx + Lss)
            index = [x + y for x, y in zip(index, increment)] # index+increment就是下一条管状线段的表皮和芯线的索引

        return L0
    
    def expand_resistance_matrix(self):
        # 扩展电阻矩阵
        coreWires_resistance_matrix = np.zeros((len(self.wires.tube_wires) * (self.wires.tube_wires[0].inner_num), len(self.wires.tube_wires) * (self.wires.tube_wires[0].inner_num)))
        self.resistance_matrix = block_diag(self.resistance_matrix, coreWires_resistance_matrix) # 增加芯线的电阻矩阵，此处只做扩充，不做芯线本身的电阻填充

    def update_resistance_matrix_by_tubeWires(self, Rin, Rx):
        # 与电感矩阵更新逻辑相同
        index = self.wires.get_tubeWires_start_index()
        increment = self.wires.get_tubeWires_index_increment()

        R0 = Rin.copy()
        R0[0, 0] = 0
        Rss = Rin[0, 0] # 此处与电感矩阵更新过程不同，此处不需要表皮的单位电阻
        for i in range(len(self.wires.tube_wires)):
            self.resistance_matrix = update_matrix(self.resistance_matrix, index, R0 + Rx + Rss)
            index = [x + y for x, y in zip(index, increment)]

    def update_capacitance_matrix_by_tubeWires(self, Cin):
        # 更新电容矩阵
        C0 = update_and_sum_matrix(Cin)
        indices = self.wires.get_tubeWires_points_index()
        for i in range(len(indices)):
            # 将C矩阵相应位置的点 更新为C0相应位置的数据
            self.capacitance_matrix = update_matrix(self.capacitance_matrix, indices[i], 0.5*C0 if i==0 or i==len(indices)-1 else C0)#与外界相连接的部分，需要折半