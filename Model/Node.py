#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re


class Node:
    def __init__(self, name, x, y, z):
        """
        初始化节点对象。
        
        参数:
        name (str): 节点的名称
        x (float): 节点的x坐标
        y (float): 节点的y坐标
        z (float): 节点的z坐标
        """
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.id = int(re.findall(r'\d+', self.name)[-1])


    def __repr__(self):
        """
        返回节点对象的字符串表示形式。
        """
        return f"Node(name='{self.name}', x={self.x}, y={self.y}, z={self.z})"


class MeasurementNode(Node):
    def __init__(self, name, x, y, z, type):
        """
        初始化测量节点对象
        
        继承自Node类, 新增参数:
        type (Int): 测量内容(电流I=1,电压V=2,P=3,All=4,能量E=11)
        
        """
        super().__init__(name, x, y, z)
        self.type = type

    def __repr__(self):
        """
        返回测量节点对象的字符串表示形式。
        """
        return f"Node(name='{self.name}', x={self.x}, y={self.y}, z={self.z}, type={self.type})"