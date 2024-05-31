import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from Info import Info
from Wires import Wires
from Lump import Circuit
from Ground import Ground
from Device import Device
from Node import MeasurementNode


class Tower:
    def __init__(self, Info: Info, Wires: Wires, Lump: Circuit, Ground: Ground, Device: Device, MeasurementNode: MeasurementNode):
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