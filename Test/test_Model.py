import sys
sys.path.append('..')
import unittest
from Model.Node import Node, MeasurementNode
from Model.Wires import Wire, TubeWire, Wires


# 测试Node类和Wire类
class TestNodeWire(unittest.TestCase):
    def test_node_initialization(self):
        # 测试Node类的初始化
        node = Node("X01", 1.0, 2.0, 3.0)
        self.assertEqual(node.name, "X01")
        self.assertEqual(node.x, 1.0)
        self.assertEqual(node.y, 2.0)
        self.assertEqual(node.z, 3.0)

    
    def test_node_initialization(self):
        # 测试MeasurementNode类的初始化
        node = MeasurementNode("X01", 1.0, 2.0, 3.0, 1)
        self.assertEqual(node.name, "X01")
        self.assertEqual(node.x, 1.0)
        self.assertEqual(node.y, 2.0)
        self.assertEqual(node.z, 3.0)
        self.assertEqual(node.type, 1)


    def test_wire_initialization(self):
        # 测试Wire类的初始化
        node1 = Node("X01", 10.5, 20.3, 15.7)
        node2 = Node("X02", -5.2, 8.9, 2.1)
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


    def test_get_node_names_and_coordinates(self):
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

        # 测试包含线段的Wires对象
        wires = Wires([air_wire], [], [tube_wire], [], [])

        expected_node_names = ['X01', 'X02', 'X03', 'X04']
        expected_coordinates = [(10.5, 20.3, 15.7), (-5.2, 8.9, 2.1), (-5.0, 8.0, 2.0), (-15.2, 18.9, 12.1)]

        self.assertEqual(wires.get_node_names(), expected_node_names)
        self.assertEqual(wires.get_node_coordinates(), expected_coordinates)



if __name__ == '__main__':
    unittest.main()