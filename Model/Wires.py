#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import math
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
from Node import Node
# from Lump import Component

class Wire:
    def __init__(self, name: str, node1: Node, node2: Node, offset: float, r: float, R: float, l: float, sig: float, mur: float, epr: float, VF: int):
        """
        初始化管状线段对象
        
        参数说明:
        name (str): 线的名称
        node1 (Node): 线的第一个节点
        node2 (Node): 线的第二个节点
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
        self.node1 = node1
        self.node2 = node2
        self.offset = offset
        self.r = r
        self.R = R
        self.L = l
        self.sig = sig
        self.mur = mur
        self.epr = epr
        self.VF = VF
        self.inner_num = 1


    def length(self):
        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        dz = self.node2.z - self.node1.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


    def __repr__(self):
        """
        返回线段对象的字符串表示形式。
        """
        return f"Wire(name='{self.name}', node1={self.node1}, node2={self.node2}, offset={self.offset}, r={self.r}, R={self.R}, L={self.L}, sig={self.sig}, mur={self.mur}, epr={self.epr}, inner_num={self.inner_num}, VF_matrix is not showned here.)"


class TubeWire(Wire):
    def __init__(self, name: str, node1: Node, node2: Node, offset: float, r: float, R: float, l: float, sig: float, mur: float, epr: float, VF: int, outer_radius: float, overall_outer_radius: float, inner_radius: float, inner_offset: float, inner_angle: float):
        """
        初始化管状线段对象。
        
        继承自Wire类,并添加或修改以下参数:
        原先的r参数表示为内径
        outer_radius (float): 外径
        overall_outer_radius (float): 整体外径
        inner_radius (float): 芯线的半径
        inner_offset (float): 芯线距离中心位置
        inner_angle (float): 芯线角度
        """
        super().__init__(name, node1, node2, offset, r, R, l, sig, mur, epr, VF)
        self.outer_radius = outer_radius
        self.overall_outer_radius = overall_outer_radius
        self.inner_radius = inner_radius
        self.inner_offset = inner_offset
        self.inner_angle = inner_angle
        self.inner_num = 4

    def __repr__(self):
        """
        返回管状线段对象的字符串表示形式。
        """
        return f"TubeWire(name='{self.name}', node1={self.node1}, node2={self.node2}, offset={self.offset}, r={self.r}, R={self.R}, L={self.L}, sig={self.sig}, mur={self.mur}, epr={self.epr}, inner_num={self.inner_num}, outer_radius={self.outer_radius}, overall_outer_radius={self.overall_outer_radius}, inner_radius={self.inner_radius}, inner_offset={self.inner_offset}, inner_angle={self.inner_angle}, VF_matrix is not showned here.)"
    


class OHLWire(Wire):
    def __init__(self, name, node1, node2, offset, r, R, l, sig, mur, epr, VF, Cir_No, Phase, phase):
        """
        初始化管状线段对象。
        
        继承自Wire类,并添加或修改以下参数:
        Cir_No (int): 线圈回路号
        Phase (str): 线圈相线
        phase (int): 线圈相数

        """
        super().__init__(name, node1, node2, offset, r, R, l, sig, mur, epr, VF)
        self.Cir_No = Cir_No
        self.Phase = Phase
        self.phase = phase


class LumpWire(Wire):
    def __init__(self, name, node1, node2, offset, r, R, l, sig, mur, epr, VF):
        """
        初始化管状线段对象。
        
        继承自Wire类,并添加以下参数:
        component(list):表示当前导线上的集中参数元件。

        """
        super().__init__(name, node1, node2, offset, r, R, l, sig, mur, epr, VF)
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

    
    def get_node_names(self):
        """
        返回结点名字列表,按照air、ground、tube、a2g、short的顺序。

        返回:
        node_names (list): 结点名字列表
        """
        node_names = []

        # 处理空气线段
        for wire in self.air_wires:
            node_names.extend([wire.node1.name, wire.node2.name])

        # 处理地线段
        for wire in self.ground_wires:
            node_names.extend([wire.node1.name, wire.node2.name])

        # 处理管状线段
        for wire in self.tube_wires:
            node_names.extend([wire.node1.name, wire.node2.name])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            node_names.extend([wire.node1.name, wire.node2.name])

        # 处理短路线段
        for wire in self.short_wires:
            node_names.extend([wire.node1.name, wire.node2.name])

        return node_names

    def get_node_coordinates(self):
        """
        返回结点坐标列表,按照air、ground、tube、a2g、short的顺序。

        返回:
        coordinates (list): 结点坐标列表,每个元素为(x, y, z)
        """
        coordinates = []

        # 处理空气线段
        for wire in self.air_wires:
            coordinates.extend([(wire.node1.x, wire.node1.y, wire.node1.z),
                                (wire.node2.x, wire.node2.y, wire.node2.z)])

        # 处理地线段
        for wire in self.ground_wires:
            coordinates.extend([(wire.node1.x, wire.node1.y, wire.node1.z),
                                (wire.node2.x, wire.node2.y, wire.node2.z)])

        # 处理管状线段
        for wire in self.tube_wires:
            coordinates.extend([(wire.node1.x, wire.node1.y, wire.node1.z),
                                (wire.node2.x, wire.node2.y, wire.node2.z)])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            coordinates.extend([(wire.node1.x, wire.node1.y, wire.node1.z),
                                (wire.node2.x, wire.node2.y, wire.node2.z)])

        # 处理短路线段
        for wire in self.short_wires:
            coordinates.extend([(wire.node1.x, wire.node1.y, wire.node1.z),
                                (wire.node2.x, wire.node2.y, wire.node2.z)])

        return coordinates
    

    def get_bran_coordinates(self):
        """
        返回按照下列格式所有线段（支路）的信息汇总列表：【线段名，起始节点名，终止节点名】,按照air、ground、tube、a2g、short的顺序。

        返回:
        coordinates (list): 结点坐标列表,每个元素为(x, y, z)
        """
        coordinates = []

        # 处理空气线段
        for wire in self.air_wires:
            coordinates.extend([(wire.name, wire.node1.name, wire.node2.name)])

        # 处理地线段
        for wire in self.ground_wires:
            coordinates.extend([(wire.name, wire.node1.name, wire.node2.name)])

        # 处理管状线段
        for wire in self.tube_wires:
            coordinates.extend([(wire.name, wire.node1.name, wire.node2.name)])

        # 处理空气到地线段
        for wire in self.a2g_wires:
            coordinates.extend([(wire.name, wire.node1.name, wire.node2.name)])

        # 处理短路线段
        for wire in self.short_wires:
            coordinates.extend([(wire.name, wire.node1.name, wire.node2.name)])

        return coordinates
    

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
                dx = (wire.node2.x - wire.node1.x) / num_segments
                dy = (wire.node2.y - wire.node1.y) / num_segments
                dz = (wire.node2.z - wire.node1.z) / num_segments
                # 获取当前即将被分割线段的起始节点
                node1 = wire.node1
                # 迭代切割线段，并分为小线段添加到线段列表中
                for i in range(num_segments):
                    # 如果是最后一个分段，则将终止节点设为线段的终止节点
                    if i == num_segments-1:
                        node2 = wire.node2
                    else:
                        node2 = Node(f"{wire.name}_MiddleNode_{i}", node1.x + dx, node1.y + dy, node1.z + dz)
                    new_wire = Wire(f"{wire.name}_Splited_{i}", node1, node2, wire.offset, wire.r, wire.R, wire.L, wire.sig, wire.mur, wire.epr, wire.VF)
                    new_wires.append(new_wire)
                    node1 = node2

        return new_wires

    def split_long_wires_all(self, max_length):
        self.air_wires = self.split_long_wires(self.air_wires, max_length)
        self.ground_wires = self.split_long_wires(self.ground_wires, max_length)
        self.a2g_wires = self.split_long_wires(self.a2g_wires, max_length)
        self.short_wires = self.split_long_wires(self.short_wires, max_length)
        self.tube_wires = self.split_long_wires(self.tube_wires, max_length)


    def __repr__(self):
        return f"Wires(air_wires={self.air_wires}, ground_wires={self.ground_wires}, a2g_wires={self.a2g_wires}, short_wires={self.short_wires}, tube_wires={self.tube_wires})"