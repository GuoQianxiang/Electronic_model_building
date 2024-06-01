import sys
sys.path.append('..')
import unittest
from Model.Node import Node, MeasurementNode
from Model.Wires import Wire, TubeWire, Wires, LumpWire
from Model.Ground import Ground
from Model.Cable import Cable
from Model.OHL import OHL
from Model.Lump import Circuit, Resistor
from Model.Tower import Tower
from Model.Info import TowerInfo
from Model.Device import Device



# 测试Node类和Wire类
class TestNodeWire(unittest.TestCase):

    def test_node_initialization(self):
        # 测试Node类的初始化
        node = Node("X01", 1.0, 2.0, 3.0)
        self.assertEqual(node.name, "X01")
        self.assertEqual(node.x, 1.0)
        self.assertEqual(node.y, 2.0)
        self.assertEqual(node.z, 3.0)

    
    def test_MeasurementNode_initialization(self):
        # 测试MeasurementNode类的初始化
        node = MeasurementNode("X01", 1.0, 2.0, 3.0, 1)
        self.assertEqual(node.name, "X01")
        self.assertEqual(node.x, 1.0)
        self.assertEqual(node.y, 2.0)
        self.assertEqual(node.z, 3.0)
        self.assertEqual(node.type, 1)


    def test_wire_initialization(self):
        # 测试Wire类的初始化
        node1 = Node("X01", 0, 0, 0)
        node2 = Node("X02", 2, 0, 0)
        wire = Wire("Test Wire", node1, node2, 1.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None)

        self.assertEqual(wire.name, "Test Wire")
        self.assertEqual(wire.node1, node1)
        self.assertEqual(wire.node2, node2)
        self.assertEqual(wire.r, 1.0)
        self.assertEqual(wire.R, 2.0)
        self.assertEqual(wire.L, 3.0)
        self.assertEqual(wire.sig, 4.0)
        self.assertEqual(wire.mur, 5.0)
        self.assertEqual(wire.epr, 6.0)
        self.assertEqual(wire.VF, None)
        self.assertEqual(wire.length(), 2.0)
        # 测试静态变量
        self.assertEqual(wire.inner_num, 1)


    def test_tube_wire_initialization(self):
        # 测试TubeWire类的初始化
        node1 = Node("Node A", 10.5, 20.3, 15.7)
        node2 = Node("Node B", -5.2, 8.9, 2.1)
        tube_wire = TubeWire("Test Tube Wire", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)

        self.assertEqual(tube_wire.name, "Test Tube Wire")
        self.assertEqual(tube_wire.node1, node1)
        self.assertEqual(tube_wire.node2, node2)
        self.assertEqual(tube_wire.r, 0.5)
        self.assertEqual(tube_wire.R, 10.0)
        self.assertEqual(tube_wire.L, 1e-9)
        self.assertEqual(tube_wire.sig, 1e7)
        self.assertEqual(tube_wire.mur, 1.0)
        self.assertEqual(tube_wire.epr, 2.1)
        self.assertEqual(tube_wire.VF, [1, 2, 3, 4])
        self.assertEqual(tube_wire.outer_radius, 1.0)
        self.assertEqual(tube_wire.overall_outer_radius, 1.5)
        self.assertEqual(tube_wire.inner_radius, 0.2)
        self.assertEqual(tube_wire.inner_offset, 0.3)
        self.assertEqual(tube_wire.inner_angle, 45.0)
        # 测试重写后的静态变量
        self.assertEqual(tube_wire.inner_num, 4)


    def test_wires_initialization(self):
        # 创建测试数据
        node1 = Node("Node A", 10.5, 20.3, 15.7)
        node2 = Node("Node B", -5.2, 8.9, 2.1)
        air_wire = Wire("Air Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        tube_wire = TubeWire("Tube Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)

        # 测试默认初始化
        wires = Wires()
        self.assertEqual(wires.air_wires, [])
        self.assertEqual(wires.ground_wires, [])
        self.assertEqual(wires.a2g_wires, [])
        self.assertEqual(wires.short_wires, [])
        self.assertEqual(wires.tube_wires, [])

        # 测试参数初始化
        wires = Wires([air_wire], [], [], [], [tube_wire])
        self.assertEqual(wires.air_wires, [air_wire])
        self.assertEqual(wires.ground_wires, [])
        self.assertEqual(wires.a2g_wires, [])
        self.assertEqual(wires.short_wires, [])
        self.assertEqual(wires.tube_wires, [tube_wire])


    def test_Wires_method(self):
        # 创建测试数据
        node1 = Node("X01", 10.5, 20.3, 15.7)
        node2 = Node("X02", -5.2, 8.9, 2.1)
        node3 = Node("X03", -5.0, 8.0, 2.0)
        node4 = Node("X04", -15.2, 18.9, 12.1)
        air_wire = Wire("Air Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        tube_wire = TubeWire("Tube Wire 1", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)

        # 测试空的Wires对象
        empty_wires = Wires()
        self.assertEqual(empty_wires.get_node_names(), [])
        self.assertEqual(empty_wires.get_node_coordinates(), [])
        self.assertEqual(empty_wires.get_bran_coordinates(), [])

        # 测试包含线段的Wires对象
        wires = Wires([air_wire], [], [tube_wire], [], [])

        expected_node_names = ['X01', 'X02', 'X03', 'X04']
        expected_coordinates = [(10.5, 20.3, 15.7), (-5.2, 8.9, 2.1), (-5.0, 8.0, 2.0), (-15.2, 18.9, 12.1)]
        expected_bran_coordinates = [("Air Wire 1", 'X01', 'X02'), ("Tube Wire 1", 'X03', 'X04')]

        self.assertEqual(wires.get_node_names(), expected_node_names)
        self.assertEqual(wires.get_node_coordinates(), expected_coordinates)
        self.assertEqual(wires.get_bran_coordinates(), expected_bran_coordinates)


    def test_Wires_split(self):
        node1 = Node('X01', 0, 0, 0)
        node2 = Node('X02', 10, 0, 0)
        node3 = Node('X03', 0, 0, 0)
        node4 = Node('X04', 15, 0, 0)
        air_wire = Wire("Y01", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        tube_wire = TubeWire("Y02", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)
        # 创建Wires对象
        wires = Wires([air_wire], [], [], [], [tube_wire])

        # 分割长度超过5m的线段
        wires.split_long_wires_all(5)
        # 最大长度为5，第一个线段应该被切割成两段
        self.assertEqual(len(wires.air_wires), 2)
        # 第二个线段应该被切割成三段
        self.assertEqual(len(wires.tube_wires), 3)
        
        # 测试第一条线段应该被分为两条线段
        # 子线段1：起始坐标是原线段的起始坐标，终止节点坐标应该是（5.0, 0.0, 0.0）,名字应该是'原来的支路名字_MiddleNode_子线段序号'
        self.assertEqual(wires.air_wires[0].node1, node1)
        self.assertEqual(wires.air_wires[0].node2.name, 'Y01_MiddleNode_0')
        self.assertEqual(wires.air_wires[0].node2.x, 5.0)
        self.assertEqual(wires.air_wires[0].node2.y, 0.0)
        self.assertEqual(wires.air_wires[0].node2.z, 0.0)

        # 子线段2：起始坐标是子线段1的终止坐标，终止节点坐标是原线段的终止坐标
        self.assertEqual(wires.air_wires[1].node1.name, 'Y01_MiddleNode_0')
        self.assertEqual(wires.air_wires[1].node1.x, 5.0)
        self.assertEqual(wires.air_wires[1].node1.y, 0.0)
        self.assertEqual(wires.air_wires[1].node1.z, 0.0)
        self.assertEqual(wires.air_wires[1].node2, node2)


class TestTower(unittest.TestCase):
    def test_Tower_initialization(self):
        # 创建节点数据
        node1 = Node("X01", 10.5, 20.3, 15.7)
        node2 = Node("X02", -5.2, 8.9, 2.1)
        node3 = Node("X03", -5.0, 8.0, 2.0)
        node4 = Node("X04", -15.2, 18.9, 12.1)

        # 创建线段数据
        air_wire = Wire("Air Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        tube_wire = TubeWire("Tube Wire 1", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)

        # 创建线段集合数据
        wires = Wires([air_wire], [], [tube_wire], [], [])

        # 创建信息集合
        vclass = "123"
        center_node = Node("Center", 1.0, 2.0, 3.0)
        Theta = 45.0
        Mode_Con = 1
        Mode_Gnd = 2
        Pole_Height = 100.0
        Pole_Head_Node = Node("Pole Head Node", 1.0, 2.0, 103.0)
        towerInfo = TowerInfo("Tower1", 1, "common tower", vclass, center_node, Theta, Mode_Con, Mode_Gnd, Pole_Height, Pole_Head_Node)

        # 创建地面参数集合
        ground = Ground(1.0, 1.0, 1.0, "ground_model", "weak","ionisation_model")

        # 创建Lump集中参数元件类
        lump = Circuit()
        # 创建一个电阻
        resistor = Resistor("Resistor_1", 100)
        # 创建导线
        wire_1 = LumpWire("Lump Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        wire_2 = LumpWire("Lump Wire 2", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        
        # 为电路图中添加导线
        lump.add_wire(wire_1)
        lump.add_wire(wire_2)
        # 为电路图添加集中参数元件（电阻）
        lump.add_component(resistor)
        # 将电阻置于导线上
        lump.connect_component_to_wire(resistor, wire_1)

        # 创建Tower对象
        measurementNode = MeasurementNode("node1", 1.0, 2.0, 3.0, 1)
        device = Device(12, 1, 0)

        tower = Tower(towerInfo, wires, lump, ground, device, measurementNode)

        expected_node_names = ['X01', 'X02', 'X03', 'X04']
        expected_coordinates = [(10.5, 20.3, 15.7), (-5.2, 8.9, 2.1), (-5.0, 8.0, 2.0), (-15.2, 18.9, 12.1)]
        expected_bran_coordinates = [("Air Wire 1", 'X01', 'X02'), ("Tube Wire 1", 'X03', 'X04')]

        self.assertEqual(tower.nodesList, expected_node_names)
        self.assertEqual(tower.nodesPositions, expected_coordinates)
        self.assertEqual(tower.bransList, expected_bran_coordinates)
        self.assertEqual(resistor.parameters['resistance'], 100)
        self.assertEqual(tower.lump.components[0].parameters, {'resistance':100})
        self.assertEqual(tower.lump.wires[0].components[0], resistor)



if __name__ == '__main__':
    unittest.main()