#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import sys
import math
import numpy as np
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
from Node import Node
# from Lump import Component
import collections

class Wire:
    def __init__(self, name: str, start_node: Node, end_node: Node, offset: float, r: float, R: float, L: float, sig: float, mur: float, epr: float, VF):
        """
        初始化管状线段对象
        
        参数说明:
        name (str): 线的名称
        start_node (Node): 线的第一个节点
        end_node (Node): 线的第二个节点
        offset (float): 线的偏置
        r (float): 线的半径
        R (float): 线的电阻
        L (float): 线的电感
        sig (float): 线的电导率
        mur (float): 线的磁导率
        epr (float): 线的相对介电常数
        VF (int): 线的向量拟合矩阵
        inner_num (int): 线的内部导体数量
        """
        self.name = name
        self.start_node = start_node
        self.end_node = end_node
        self.offset = offset
        self.r = r
        self.R = R
        self.L = L
        self.sig = sig
        self.mur = mur
        self.epr = epr
        self.VF = VF
        self.inner_num = 1
        self.height = (end_node.z + start_node.z)/2


    def length(self):
        dx = self.end_node.x - self.start_node.x
        dy = self.end_node.y - self.start_node.y
        dz = self.end_node.z - self.start_node.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


    def display(self):
        """
        打印线段对象信息。
        """
        print(f"Wire(name='{self.name}', start_node={self.start_node}, end_node={self.end_node}, offset={self.offset}, r={self.r}, R={self.R}, L={self.L}, sig={self.sig}, mur={self.mur}, epr={self.epr}, inner_num={self.inner_num}, VF_matrix is not showned here.)\n")


    def __repr__(self):
        """
        返回线段对象的字符串表示形式。
        """
        return f"Wire(name='{self.name}', start_node={self.start_node}, end_node={self.end_node}, offset={self.offset}, r={self.r}, R={self.R}, L={self.L}, sig={self.sig}, mur={self.mur}, epr={self.epr}, inner_num={self.inner_num}, VF_matrix is not showned here.)"


class CoreWire(Wire):
    def __init__(self, name: str, start_node: Node, end_node: Node, offset: float, r: float, R: float, L: float, sig: float, mur: float, epr: float, VF, inner_offset: float, inner_angle: float):
        """
        初始化管状线内部的芯线线段。

        继承自Wire类,并添加以下参数:
        inner_offset (float): 芯线距离中心的位置
        inner_angle (float): 芯线的偏转角度
        """
        super().__init__(name, start_node, end_node, offset, r, R, L, sig, mur, epr, VF)
        self.inner_offset = inner_offset
        self.inner_angle = inner_angle
    

    def display(self):
        """
        打印线段对象信息。
        """
        print(f"    CoreWire(name='{self.name}', start_node={self.start_node}, end_node={self.end_node}, offset={self.offset}, r={self.r}, R={self.R}, L={self.L}, sig={self.sig}, mur={self.mur}, epr={self.epr}, inner_num={self.inner_num}, VF_matrix is not showned here, inner_angle={self.inner_angle}, inner_offset={self.inner_offset})\n")


class TubeWire():
    def __init__(self, sheath: Wire, inner_radius: float, outer_radius: float, inner_num: int):
        """
        初始化管状线段对象。(同时满足cable中线段的定义)
        
        inner_radius (float): 不加套管厚度的内部外径
        outer_radius (float): 添加了套管厚度的整体外径
        inner_num (int): 内部芯线的数量
        """
        self.sheath = sheath
        self.core_wires = []
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.inner_num = inner_num


    def add_core_wire(self, wire: CoreWire):
        """
        向管状线段中添加内部芯线线段。

        Args:
            wire (Wire): 要添加的芯线线段。
        """
        if len(self.core_wires) >= self.inner_num:
            raise ValueError("TubeWire can only have {} inner wires, but {} is added.".format(self.inner_num, len(self.core_wires) + 1))
        self.core_wires.append(wire)


    def display(self):
        """
        打印管状线段信息。
        """
        print(f"TubeWire(sheath={self.sheath}, inner_radius={self.inner_radius}, outer_radius={self.outer_radius}, inner_num={self.inner_num})\n")
        for corewire in self.core_wires:
            corewire.display()


    def get_coreWires_radii(self):
        """
        返回芯线集合的半径矩阵。

        返回:
        radii (numpy.narray, n*1): n条芯线的半径矩阵,每行为某一条芯线的半径
        """
        radii = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            radii[i] = wire.r
        return radii

    def get_coreWires_endNodeZ(self):
        """
        返回芯线末端z值矩阵。

        返回:
        end_node_z (numpy.narray, n*1): n条芯线的末端z值
        """
        end_node_z = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            end_node_z[i] = wire.end_node.z
        return end_node_z

    def get_coreWires_sig(self):
        """
        返回芯线电导率矩阵。

        返回:
        sig (numpy.narray, n*1): n条芯线的电导率
        """
        sig = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            sig[i] = wire.sig
        return sig

    def get_coreWires_mur(self):
        """
        返回芯线磁导率。

        返回:
        mur (numpy.narray, n*1): n条芯线的磁导率
        """
        mur = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            mur[i] = wire.mur
        return mur

    def get_coreWires_epr(self):
        """
        返回芯线相对介电常数。

        返回:
        epr (numpy.narray, n*1): n条芯线的相对介电常数
        """
        epr = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            epr[i] = wire.epr
        return epr

    def get_coreWires_innerOffset(self):
        """
        返回芯线偏置矩阵。

        返回:
        inner_offset (numpy.narray, n*1): n条芯线的偏置
        """
        inner_offset = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            inner_offset[i] = wire.inner_offset
        return inner_offset

    def get_coreWires_innerAngle(self):
        """
        返回芯线角度矩阵。

        返回:
        inner_angle (numpy.narray, n*1): n条芯线的角度
        """
        inner_angle = np.zeros((len(self.core_wires), 1))
        for i, wire in enumerate(self.core_wires):
            inner_angle[i] = wire.inner_angle
        return inner_angle


class OHLWire(Wire):
    def __init__(self, name, start_node, end_node, offset, r, R, l, sig, mur, epr, VF, Cir_No, Phase, phase):
        """
        初始化管状线段对象。
        
        继承自Wire类,并添加或修改以下参数:
        Cir_No (int): 线圈回路号
        Phase (str): 线圈相线
        phase (int): 线圈相数

        """
        super().__init__(name, start_node, end_node, offset, r, R, l, sig, mur, epr, VF)
        self.Cir_No = Cir_No
        self.Phase = Phase
        self.phase = phase


class LumpWire(Wire):
    def __init__(self, name, start_node, end_node, offset, r, R, l, sig, mur, epr, VF):
        """
        初始化管状线段对象。

        继承自Wire类,并添加以下参数:
        component(list):表示当前导线上的集中参数元件。

        """
        super().__init__(name, start_node, end_node, offset, r, R, l, sig, mur, epr, VF)
        self.components = []

    def add_component(self, component):
        """
        将一个基础元件添加到该导线上。

        Args:
            component (Component): 要添加的基础元件对象。
        """
        self.components.append(component)


class Wires:
    def __init__(self, air_wires=None, ground_wires=None, a2g_wires=None, short_wires=None, tube_wires=None):
        """
        初始化Wires对象

        参数:
        air_wires (Wire类型的list, optional): 空气线段列表,默认为空列表。
        ground_wires (Wire类型的list, optional): 地线段列表,默认为空列表。
        a2g_wires (Wire类型的list, optional): 空气到地线段列表,默认为空列表。
        short_wires (Wire类型的list, optional): 短路线段列表,默认为空列表。
        tube_wires (TubeWire类型的list, optional): 管状线段列表,默认为空列表。
        """
        self.air_wires = air_wires or []
        self.ground_wires = ground_wires or []
        self.a2g_wires = a2g_wires or []
        self.short_wires = short_wires or []
        self.tube_wires = tube_wires or []


    def display(self):
        # 处理空气线段
        print("[air_wires]:\n")
        for wire in self.air_wires:
            wire.display()

        # 处理地线段
        print("[ground_wires]:\n")
        for wire in self.ground_wires:
            wire.display()

        # 处理管状线段
        print("[tube_wires]:\n")
        for wire in self.tube_wires:
            wire.display()

        # 处理空气到地线段
        print("[a2g_wires]:\n")
        for wire in self.a2g_wires:
            wire.display()

        # 处理短路线段
        print("[short_wires]:\n")
        for wire in self.short_wires:
            wire.display()


    def add_air_wire(self, wire):
        self.air_wires.append(wire)

    def add_ground_wire(self, wire):
        self.ground_wires.append(wire)

    def add_a2g_wire(self, wire):
        self.a2g_wires.append(wire)

    def add_short_wire(self, wire):
        self.short_wires.append(wire)

    def add_tube_wire(self, wire):
        self.tube_wires.append(wire)

    def count(self):
        """
        返回线段总数。
        """
        # 由于业务需要，tubeWire的表皮默认存在于air_wire中，此处num_tubeWires只统计内部芯线的数量
        num_tubeWires = 0
        for i in range(len(self.tube_wires)):
            num_tubeWires += self.tube_wires[i].inner_num
        return len(self.air_wires) + len(self.ground_wires) + num_tubeWires + len(self.a2g_wires) + len(self.short_wires)


    def get_node_names(self):
        """
        返回结点名字列表,按照air、ground、tube、a2g、short的顺序。

        返回:
        node_names (list): 结点名字列表
        """
        node_names = []

        # 要求按照特定顺序进行拼接，因此分别进行for循环。

        # 处理空气线段
        for wire in self.air_wires:
            node_names.extend([wire.start_node.name, wire.end_node.name])

        # 处理地线段
        for wire in self.ground_wires:
            node_names.extend([wire.start_node.name, wire.end_node.name])

        # 处理管状线段
        for wire in self.tube_wires:
            node_names.extend([wire.sheath.start_node.name, wire.sheath.end_node.name])
            for core_wire in wire.core_wires:
                node_names.extend([core_wire.start_node.name, core_wire.end_node.name])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            node_names.extend([wire.start_node.name, wire.end_node.name])

        # 处理短路线段
        for wire in self.short_wires:
            node_names.extend([wire.start_node.name, wire.end_node.name])

        return node_names

    def get_node_coordinates(self):
        """
        返回结点坐标列表,按照air、ground、tube、a2g、short的顺序。

        返回:
        coordinates (list): 结点坐标列表,每个元素为(x, y, z)
        """
        coordinates = []

        # 要求按照特定顺序进行拼接，因此分别进行for循环。

        # 处理空气线段
        for wire in self.air_wires:
            coordinates.extend([(wire.start_node.x, wire.start_node.y, wire.start_node.z),
                                (wire.end_node.x, wire.end_node.y, wire.end_node.z)])

        # 处理地线段
        for wire in self.ground_wires:
            coordinates.extend([(wire.start_node.x, wire.start_node.y, wire.start_node.z),
                                (wire.end_node.x, wire.end_node.y, wire.end_node.z)])

        # 处理管状线段
        for tubewire in self.tube_wires:
            coordinates.extend([(tubewire.sheath.start_node.x, tubewire.sheath.start_node.y, tubewire.sheath.start_node.z),
                                (tubewire.sheath.end_node.x, tubewire.sheath.end_node.y, tubewire.sheath.end_node.z)])
            for core_wire in tubewire.core_wires:
                coordinates.extend([(core_wire.start_node.x, core_wire.start_node.y, core_wire.start_node.z),
                                    (core_wire.end_node.x, core_wire.end_node.y, core_wire.end_node.z)])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            coordinates.extend([(wire.start_node.x, wire.start_node.y, wire.start_node.z),
                                (wire.end_node.x, wire.end_node.y, wire.end_node.z)])

        # 处理短路线段
        for wire in self.short_wires:
            coordinates.extend([(wire.start_node.x, wire.start_node.y, wire.start_node.z),
                                (wire.end_node.x, wire.end_node.y, wire.end_node.z)])

        return coordinates


    def count_distinct_airPoints(self):
        """
        统计 Wires 对象中所有空气线段的起始点和终止点的总个数。

        参数:
        wires (Wires): Wires 对象

        返回:
        int: 所有不重复点的总个数
        """
        all_points = set()

        # 统计 air_wires 中的点
        for wire in self.air_wires:
            all_points.add(wire.start_node)
            all_points.add(wire.end_node)

        return len(all_points)


    def count_distinct_gndPoints(self) -> int:
        """
        统计 Wires 对象中所有地线段的起始点和终止点的总个数。

        参数:
        wires (Wires): Wires 对象

        返回:
        int: 所有不重复点的总个数
        """
        all_points = set()

        # 统计 ground_wires 中的点
        for wire in self.ground_wires:
            all_points.add(wire.start_node)
            all_points.add(wire.end_node)

        return len(all_points)


    def count_distinct_points(self) -> int:
        """
        统计 Wires 对象中所有线段的起始点和终止点的总个数。

        参数:
        wires (Wires): Wires 对象

        返回:
        int: 所有不重复点的总个数
        """
        return len(self.get_all_nodes())

    
    def get_all_nodes(self):
        """
        返回 Wires 对象中所有线段的所有点的集合。

        参数:
        wires (Wires): Wires 对象

        返回:
        all_nodes(OrderedDict): 所有不重复点的有序集合
        """
        # 获取所有不重复的节点(包含管状线段内部线段的起始点和终止点)
        all_nodes = collections.OrderedDict()
        for wire_list in [self.air_wires, self.ground_wires, self.a2g_wires, self.short_wires]:
            for wire in wire_list:
                all_nodes[wire.start_node] = True
                all_nodes[wire.end_node] = True

        for tubewire in self.tube_wires:
            all_nodes[tubewire.sheath.start_node] = True
            all_nodes[tubewire.sheath.end_node] = True
            for core_wire in tubewire.core_wires:
                all_nodes[core_wire.start_node] = True
                all_nodes[core_wire.end_node] = True

        return list(all_nodes)
    

    def get_tubeWires_points_index(self):
        """
        获取管状线段在切分后 表皮和芯线起点终点的索引

        参数:
        wires (Wires): Wires 对象

        返回:
        indices(list): 二维矩阵, 按照切分的批, 分别表示一批表皮和芯线的点的索引集合
        """
        all_nodes = self.get_all_nodes()
        node_to_index = {node: i for i, node in enumerate(all_nodes)}
        indices = []
        for tubewire in self.tube_wires:
            index = []
            index.append(node_to_index[tubewire.sheath.start_node])

            for core_wire in tubewire.core_wires:
                index.append(node_to_index[core_wire.start_node])
            indices.append(index)
        index = []
        index.append(node_to_index[self.tube_wires[len(self.tube_wires)-1].sheath.end_node])
        for core_wire in self.tube_wires[len(self.tube_wires)-1].core_wires:
                index.append(node_to_index[core_wire.end_node])
        indices.append(index)
        return indices


    def count_a2gWires(self):
        return len(self.a2g_wires)


    def count_tubeWires(self):
        return len(self.tube_wires)


    def count_gndWires(self):
        return len(self.ground_wires)


    def count_airWires(self):
        return len(self.air_wires)


    def get_start_points(self):
        """
        返回起始点结点坐标矩阵,按照air、ground、a2g、short的顺序。
        管状线段单独处理,此处跳过。
        返回:
        start_points (numpy.narray, n*3): n条线段的起始点结点坐标矩阵,每行为(x, y, z)
        """
        start_points = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 3))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            start_points[i] = [wire.start_node.x, wire.start_node.y, wire.start_node.z]
        return start_points


    def get_end_points(self):
        """
        返回终止点结点坐标矩阵,按照air、ground、a2g、short的顺序。

        返回:
        end_points (numpy.narray, n*3): n条线段的终止点结点坐标矩阵,每行为(x, y, z)
        """
        end_points = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 3))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            end_points[i] = [wire.end_node.x, wire.end_node.y, wire.end_node.z]
        return end_points


    def get_radii(self):
        """
        返回线段集合的内径矩阵,按照air、ground、a2g、short的顺序。

        返回:
        radii (numpy.narray, n*1): n条线段的内径矩阵,每行为某一条线段的内径
        """
        radii = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            radii[i] = wire.r
        return radii


    def get_heights(self):
        """
        返回线段高度矩阵,按照air、ground、a2g、short的顺序。

        返回:
        heights (numpy.narray, n*1): n条线段的高度
        """
        heights = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            heights[i] = wire.height
        return heights


    def get_offsets(self):
        """
        返回线段偏置矩阵,按照air、ground、a2g、short的顺序。

        返回:
        offsets (numpy.narray, n*1): n条线段的偏置
        """
        offsets = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            offsets[i] = wire.offset
        return offsets


    def get_lengths(self):
        """
        返回线段长度矩阵,按照air、ground、a2g、short的顺序。

        返回:
        lengths (numpy.narray, n*1): n条线段的长度
        """
        lengths = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            lengths[i] = wire.length()
        return lengths


    def get_resistance(self):
        """
        返回线段电阻矩阵,按照air、ground、a2g、short的顺序。

        返回:
        impendence (numpy.narray, n*1): n条线段的电阻
        """
        resistance = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            resistance[i] = wire.R
        return resistance
    
    def get_inductance(self):
        """
        返回线段电感矩阵,按照air、ground、a2g、short、tube的顺序。

        返回:
        inductance (numpy.narray, n*1): n条线段的电感
        """
        inductance = np.zeros((len(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires), 1))
        for i, wire in enumerate(self.air_wires + self.ground_wires + self.a2g_wires + self.short_wires):
            inductance[i] = wire.L
        return inductance



    def get_bran_coordinates(self):
        """
        返回按照下列格式所有线段（支路）的信息汇总列表：【线段名，起始节点名，终止节点名】,按照air、ground、tube、a2g、short的顺序。

        返回:
        coordinates (list): 信息汇总列表,每个元素为("Y01", "X01", "X02")
        """
        coordinates = []

        # 要求按照特定顺序进行拼接，因此分别进行for循环。

        # 处理空气线段
        for wire in self.air_wires:
            coordinates.extend([(wire.name, wire.start_node.name, wire.end_node.name)])

        # 处理地线段
        for wire in self.ground_wires:
            coordinates.extend([(wire.name, wire.start_node.name, wire.end_node.name)])

        # 处理管状线段
        for tubewire in self.tube_wires:
            coordinates.extend([(tubewire.sheath.name, tubewire.sheath.start_node.name, tubewire.sheath.end_node.name)])
            for corewire in tubewire.core_wires:
                coordinates.extend([(corewire.name, corewire.start_node.name, corewire.end_node.name)])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            coordinates.extend([(wire.name, wire.start_node.name, wire.end_node.name)])

        # 处理短路线段
        for wire in self.short_wires:
            coordinates.extend([(wire.name, wire.start_node.name, wire.end_node.name)])

        return coordinates


    def get_bran_index(self):
        """
        传入一个 wire 列表,返回一个 N*2 的 NumPy 矩阵,其中 N 为 wire 的数量,
        第一列表示每条线的起始点编号,第二列表示终止点编号,编号从 1 开始,且每个点拥有全局唯一的编号。

        参数:
        wires (list): 包含 wire 对象的列表,每个 wire 对象需要有 start_node 和 end_node 属性。

        返回:
        wire_matrix (numpy.ndarray): N*2 的矩阵,其中 N 为 wire 的数量。
        """
        # 使用有序字典存储所有的节点及其编号
        node_to_index = collections.OrderedDict()
        next_index = 1

        # 遍历所有的 wire,构建节点编号字典和wire矩阵
        wire_matrix = []
        for wire in self.air_wires + self.ground_wires:
            start_node = wire.start_node
            end_node = wire.end_node

            # 如果起始节点不在字典中,添加到字典并分配编号
            if start_node not in node_to_index:
                node_to_index[start_node] = next_index
                next_index += 1

            # 如果终止节点不在字典中,添加到字典并分配编号
            if end_node not in node_to_index:
                node_to_index[end_node] = next_index
                next_index += 1

            # 将当前 wire 的起始点和终止点编号加入矩阵
            wire_matrix.append([node_to_index[start_node], node_to_index[end_node]])

        return np.array(wire_matrix)
    

    def get_tubeWires_start_index(self):
        index = [len(self.air_wires) - len(self.tube_wires)]
        for i in range(len(self.air_wires) + len(self.ground_wires) , len(self.air_wires) + len(self.ground_wires) + self.tube_wires[0].inner_num):
            index.append(i)

        return index
    
    def get_tubeWires_index_increment(self):
        increment = [1]
        inner_num = self.tube_wires[0].inner_num
        for i in range(inner_num):
            increment.append(inner_num)
        
        return increment

    def split_long_wires(self, wires, max_length):
        new_wires = []
        # 对所有的线段做长度检查
        for wire in wires:
            wire_length = wire.length()
            # 如果长度符合要求，则跳过，否则，做线段切分
            if wire_length <= max_length:
                new_wires.append(wire)
            else:
                # 计算要均匀切分为多少段
                num_segments = math.ceil(wire_length / max_length)
                # 计算每个子分段的坐标分量
                dx = (wire.end_node.x - wire.start_node.x) / num_segments
                dy = (wire.end_node.y - wire.start_node.y) / num_segments
                dz = (wire.end_node.z - wire.start_node.z) / num_segments
                # 获取当前即将被分割线段的起始节点
                start_node = wire.start_node
                # 迭代切割线段，并分为小线段添加到线段列表中
                for i in range(num_segments):
                    # 如果是最后一个分段，则将终止节点设为线段的终止节点
                    if i == num_segments-1:
                        end_node = wire.end_node
                    else:
                        end_node = Node(f"{wire.name}_MiddleNode_{i+1}", start_node.x + dx, start_node.y + dy, start_node.z + dz)
                    new_wire = Wire(f"{wire.name}_Splited_{i+1}", start_node, end_node, wire.offset, wire.r, wire.R, wire.L, wire.sig, wire.mur, wire.epr, wire.VF)
                    new_wires.append(new_wire)
                    start_node = end_node

        return new_wires
    

    def split_tubewires(self, tubewires, max_length):
        """
        将输入的 TubeWire 列表切分成长度不超过 max_length 的新 TubeWire 列表。

        参数:
        tubewires (List[TubeWire]): 需要切分的 TubeWire 列表
        max_length (float): 每个 TubeWire 的最大长度

        返回:
        List[TubeWire]: 切分后的新 TubeWire 列表
        """
        new_tubewires = []

        for tubewire in tubewires:
            sheath = tubewire.sheath
            sheath_start_node = sheath.start_node
            sheath_end_node = sheath.end_node
            length = sheath.length()

            if length <= max_length:
                new_tubewires.append(tubewire)
            else:
                # 计算切分的段数
                num_segments = math.ceil(length / max_length)
                dx = (sheath_end_node.x - sheath_start_node.x) / num_segments
                dy = (sheath_end_node.y - sheath_start_node.y) / num_segments
                dz = (sheath_end_node.z - sheath_start_node.z) / num_segments

                # 切分 sheath
                sheath_start_point = sheath_start_node
                sheath_end_point = sheath_end_node
                core_wires_middle_nodes = collections.deque()
                for i in range(num_segments):
                    middle_node = Node(name=f"{sheath.name}_MiddleNode_{i+1}",
                                       x = sheath_start_point.x + (i+1)*dx,
                                       y = sheath_start_point.y + (i+1)*dy,
                                       z = sheath_start_point.z + (i+1)*dz)

                    new_sheath = Wire(
                        name=f"{sheath.name}_Splited_{i+1}",
                        start_node=sheath_start_point,
                        end_node=sheath_end_point if i == num_segments-1 else middle_node,
                        offset=sheath.offset,
                        r=sheath.r,
                        R=sheath.R,
                        L=sheath.L,
                        sig=sheath.sig,
                        mur=sheath.mur,
                        epr=sheath.epr,
                        VF=sheath.VF
                    )
                    sheath_start_point = middle_node

                    # 切分 core_wires
                    new_core_wires = []
                    for core_wire in tubewire.core_wires:
                        start_point = core_wire.start_node
                        end_point = core_wire.end_node
                        new_core_wire = CoreWire(
                            name=f"{core_wire.name}_Splited_{i+1}",
                            start_node=start_point if i == 0 else core_wires_middle_nodes.popleft(),
                            end_node=end_point if i == num_segments-1 else Node(name=f"{core_wire.name}_MiddleNode_{i+1}",
                                                                                x = start_point.x+ (i+1)*dx,
                                                                                y = start_point.y+ (i+1)*dy,
                                                                                z = start_point.z+ (i+1)*dz),
                            offset=core_wire.offset,
                            r=core_wire.r,
                            R=core_wire.R,
                            L=core_wire.L,
                            sig=core_wire.sig,
                            mur=core_wire.mur,
                            epr=core_wire.epr,
                            VF=core_wire.VF,
                            inner_offset=core_wire.inner_offset,
                            inner_angle=core_wire.inner_angle
                        )
                        new_core_wires.append(new_core_wire)
                        core_wires_middle_nodes.append(new_core_wire.end_node)

                    new_tubewire = TubeWire(
                        sheath=new_sheath,
                        inner_radius=tubewire.inner_radius,
                        outer_radius=tubewire.outer_radius,
                        inner_num=tubewire.inner_num
                    )
                    new_tubewire.core_wires = new_core_wires
                    new_tubewires.append(new_tubewire)

        return new_tubewires


    def split_long_wires_all(self, max_length):
        self.air_wires = self.split_long_wires(self.air_wires, max_length)
        self.ground_wires = self.split_long_wires(self.ground_wires, max_length)
        self.a2g_wires = self.split_long_wires(self.a2g_wires, max_length)
        self.short_wires = self.split_long_wires(self.short_wires, max_length)
        self.tube_wires = self.split_tubewires(self.tube_wires, max_length)


    def __repr__(self):
        return f"Wires(\nair_wires={self.air_wires},\n ground_wires={self.ground_wires},\n a2g_wires={self.a2g_wires},\n short_wires={self.short_wires},\n tube_wires={self.tube_wires}\n)"