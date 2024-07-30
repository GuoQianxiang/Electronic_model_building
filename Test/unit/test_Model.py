import sys
sys.path.append('../..')
import unittest
from Model.Node import Node, MeasurementNode
from Model.Wires import Wire, TubeWire, Wires, LumpWire, CoreWire
from Model.Ground import Ground
from Model.Cable import Cable
from Model.OHL import OHL
# from Model.Lump import Circuit, Resistor
from Model.Tower import Tower
from Model.Info import TowerInfo
from Model.Device import Device
from Model.Lightning import Lightning, Stroke
import numpy as np



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
        start_node = Node("X01", 0, 0, 0)
        end_node = Node("X02", 2, 0, 0)
        wire = Wire("Test Wire", start_node, end_node, 1.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, None)

        self.assertEqual(wire.name, "Test Wire")
        self.assertEqual(wire.start_node, start_node)
        self.assertEqual(wire.end_node, end_node)
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
        # 表皮的起点和终点
        node9 = Node("X52", 10, 0, 0)
        node10 = Node("X56", 10, 0, 100)
        #三条芯线的起点和终点
        node11 = Node("X53", 10, 0, 0)
        node12 = Node("X57", 10, 0, 100)
        node13 = Node("X54", 10, 0, 0)
        node14 = Node("X58", 10, 0, 100)
        node15 = Node("X55", 10, 0, 0)
        node16 = Node("X59", 10, 0, 100)
        # 创建套管线段集合
        VF = {}
        core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, -5)
        core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 0)
        core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 5)
        sheath_wire = Wire("Y10", node9, node10, 0, 2, 0, 0, 1e7, 50, 1, VF)
        tube_wire1 = TubeWire(sheath_wire, 2.05, 2.1, 3)
        tube_wire1.add_core_wire(core_wire1)
        tube_wire1.add_core_wire(core_wire2)
        tube_wire1.add_core_wire(core_wire3)
        # 测试类变量
        self.assertEqual(tube_wire1.inner_radius, 2.05)
        self.assertEqual(tube_wire1.outer_radius, 2.1)
        self.assertEqual(tube_wire1.inner_num, 3)
        # to be tested


    def test_wires_initialization(self):
        # 创建测试数据
        start_node = Node("X01", 10.5, 20.3, 15.7)
        end_node = Node("X02", -5.2, 8.9, 2.1)
        air_wire = Wire("Air Wire 1", start_node, end_node, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        # 表皮的起点和终点
        node9 = Node("X52", 10, 0, 0)
        node10 = Node("X56", 10, 0, 100)
        #三条芯线的起点和终点
        node11 = Node("X53", 10, 0, 0)
        node12 = Node("X57", 10, 0, 100)
        node13 = Node("X54", 10, 0, 0)
        node14 = Node("X58", 10, 0, 100)
        node15 = Node("X55", 10, 0, 0)
        node16 = Node("X59", 10, 0, 100)
        # 创建套管线段集合
        VF = {}
        core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, -5)
        core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 0)
        core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 5)
        sheath_wire = Wire("Y10", node9, node10, 0, 2, 0, 0, 1e7, 50, 1, VF)
        tube_wire1 = TubeWire(sheath_wire, 2.05, 2.1, 3)
        tube_wire1.add_core_wire(core_wire1)
        tube_wire1.add_core_wire(core_wire2)
        tube_wire1.add_core_wire(core_wire3)

        # 测试默认初始化
        wires = Wires()
        self.assertEqual(wires.air_wires, [])
        self.assertEqual(wires.ground_wires, [])
        self.assertEqual(wires.a2g_wires, [])
        self.assertEqual(wires.short_wires, [])
        self.assertEqual(wires.tube_wires, [])

        # 测试参数初始化
        wires = Wires([air_wire], [], [], [], [tube_wire1])
        self.assertEqual(wires.air_wires, [air_wire])
        self.assertEqual(wires.ground_wires, [])
        self.assertEqual(wires.a2g_wires, [])
        self.assertEqual(wires.short_wires, [])
        self.assertEqual(wires.tube_wires, [tube_wire1])


# class TestTower(unittest.TestCase):
#     def test_Tower_initialization(self):
#         # 创建节点数据
#         node1 = Node("X01", 10.5, 20.3, 15.7)
#         node2 = Node("X02", -5.2, 8.9, 2.1)
#         node3 = Node("X03", -5.0, 8.0, 2.0)
#         node4 = Node("X04", -15.2, 18.9, 12.1)

#         # 创建线段数据
#         air_wire = Wire("Air Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
#         tube_wire = TubeWire("Tube Wire 1", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4], 1.0, 1.5, 0.2, 0.3, 45.0)

#         # 创建线段集合数据
#         wires = Wires([air_wire], [], [], [], [tube_wire])

#         # 创建信息集合
#         vclass = "123"
#         center_node = Node("Center", 1.0, 2.0, 3.0)
#         Theta = 45.0
#         Mode_Con = 1
#         Mode_Gnd = 2
#         Pole_Height = 100.0
#         Pole_Head_Node = Node("Pole Head Node", 1.0, 2.0, 103.0)
#         towerInfo = TowerInfo("Tower1", 1, "common tower", vclass, center_node, Theta, Mode_Con, Mode_Gnd, Pole_Height, Pole_Head_Node)

#         # 创建地面参数集合
#         ground = Ground(1.0, 1.0, 1.0, "ground_model", "weak","ionisation_model")

#         # 创建Lump集中参数元件类
#         lump = Circuit()
#         # 创建一个电阻
#         resistor = Resistor("Resistor_1", 100)
#         # 创建导线
#         wire_1 = LumpWire("Lump Wire 1", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
#         wire_2 = LumpWire("Lump Wire 2", node3, node4, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        
#         # 为电路图中添加导线
#         lump.add_wire(wire_1)
#         lump.add_wire(wire_2)
#         # 为电路图添加集中参数元件（电阻）
#         lump.add_component(resistor)
#         # 将电阻置于导线上
#         lump.connect_component_to_wire(resistor, wire_1)

#         # 创建Tower对象
#         measurementNode = MeasurementNode("start_node", 1.0, 2.0, 3.0, 1)
#         device = Device(12, 1, 0)

#         tower = Tower(towerInfo, wires, lump, ground, device, measurementNode)

#         expected_node_names = ['X01', 'X02', 'X03', 'X04']
#         expected_coordinates = [(10.5, 20.3, 15.7), (-5.2, 8.9, 2.1), (-5.0, 8.0, 2.0), (-15.2, 18.9, 12.1)]
#         expected_bran_coordinates = [("Air Wire 1", 'X01', 'X02'), ("Tube Wire 1", 'X03', 'X04')]

#         self.assertEqual(tower.nodesList, expected_node_names)
#         self.assertEqual(tower.nodesPositions, expected_coordinates)
#         self.assertEqual(tower.bransList, expected_bran_coordinates)
#         self.assertEqual(resistor.parameters['resistance'], 100)
#         self.assertEqual(tower.lump.components[0].parameters, {'resistance':100})
#         self.assertEqual(tower.lump.wires[0].components[0], resistor)


class TestWiresMethods(unittest.TestCase):
    def test_Wires_get_method(self):
        # 创建测试数据
        start_node = Node("X01", 10.5, 20.3, 15.7)
        end_node = Node("X02", -5.2, 8.9, 2.1)
        air_wire = Wire("Air Wire 1", start_node, end_node, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        
        # 表皮的起点和终点
        node9 = Node("X52", 10, 0, 0)
        node10 = Node("X56", 10, 0, 100)
        #三条芯线的起点和终点
        node11 = Node("X53", 10, 0, 0)
        node12 = Node("X57", 10, 0, 100)
        node13 = Node("X54", 10, 0, 0)
        node14 = Node("X58", 10, 0, 100)
        node15 = Node("X55", 10, 0, 0)
        node16 = Node("X59", 10, 0, 100)
        # 创建套管线段集合
        VF = {}
        core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, -5)
        core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 0)
        core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 5)
        sheath_wire = Wire("Y10", node9, node10, 0, 2, 0, 0, 1e7, 50, 1, VF)
        tube_wire1 = TubeWire(sheath_wire, 2.05, 2.1, 3)
        tube_wire1.add_core_wire(core_wire1)
        tube_wire1.add_core_wire(core_wire2)
        tube_wire1.add_core_wire(core_wire3)

        # 测试空的Wires对象
        empty_wires = Wires()
        self.assertEqual(empty_wires.get_node_names(), [])
        self.assertEqual(empty_wires.get_node_coordinates(), [])
        self.assertEqual(empty_wires.get_bran_coordinates(), [])

        # 测试包含线段的Wires对象
        wires = Wires([air_wire], [], [], [], [tube_wire1])

        expected_node_names = ['X01', 'X02', 'X52', 'X56', 'X53', 'X57', 'X54', 'X58', 'X55', 'X59']
        expected_coordinates = [(10.5, 20.3, 15.7), (-5.2, 8.9, 2.1), (10, 0, 0), (10, 0, 100), (10, 0, 0), (10, 0, 100), (10, 0, 0), (10, 0, 100), (10, 0, 0), (10, 0, 100),]
        expected_bran_coordinates = [("Air Wire 1", 'X01', 'X02'), ("Y10", 'X52', 'X56'), ("Y11", "X53", "X57"), ("Y12", "X54", "X58"), ("Y13", "X55", "X59")]

        self.assertEqual(wires.get_node_names(), expected_node_names)
        self.assertEqual(wires.get_node_coordinates(), expected_coordinates)
        self.assertEqual(wires.get_bran_coordinates(), expected_bran_coordinates)


    def test_Wires_split(self):
        # 初始化点
        node1 = Node('X01', 0, 0, 0)
        node2 = Node('X02', 10, 0, 0)
        # 根据点初始化线
        air_wire = Wire("Y01", node1, node2, 1.0, 0.5, 10.0, 1e-9, 1e7, 1.0, 2.1, [1, 2, 3, 4])
        # 表皮的起点和终点
        node9 = Node("X52", 10, 0, 0)
        node10 = Node("X56", 10, 0, 15)
        #三条芯线的起点和终点
        node11 = Node("X53", 10, 0, 0)
        node12 = Node("X57", 10, 0, 15)
        node13 = Node("X54", 10, 0, 0)
        node14 = Node("X58", 10, 0, 15)
        node15 = Node("X55", 10, 0, 0)
        node16 = Node("X59", 10, 0, 15)
        # 创建套管线段集合
        VF = {}
        core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, -5)
        core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 0)
        core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 5)
        sheath_wire = Wire("Y10", node9, node10, 0, 2, 0, 0, 1e7, 50, 1, VF)
        tube_wire1 = TubeWire(sheath_wire, 2.05, 2.1, 3)
        tube_wire1.add_core_wire(core_wire1)
        tube_wire1.add_core_wire(core_wire2)
        tube_wire1.add_core_wire(core_wire3)
        # 创建Wires对象
        wires = Wires()
        # 将导线按照其位置，添加到Wires集合中。
        wires.add_air_wire(air_wire)
        wires.add_tube_wire(tube_wire1)
        # print("----------------------------------------------------------------")
        # wires.display()
        # print("----------------------------------------------------------------")

        # 分割长度超过5m的线段
        wires.split_long_wires_all(5)
        # print("----------------------------------------------------------------")
        # wires.display()
        # print("----------------------------------------------------------------")
        # 最大长度为5，第一个线段应该被切割成两段
        self.assertEqual(len(wires.air_wires), 2)
        # 第二个线段应该被切割成三段
        self.assertEqual(len(wires.tube_wires), 3)
        
        # 测试第一条线段应该被分为两条线段
        # 子线段1：起始坐标是原线段的起始坐标，终止节点坐标应该是（5.0, 0.0, 0.0）,名字应该是'原来的支路名字_MiddleNode_子线段序号'
        self.assertEqual(wires.air_wires[0].start_node, node1)
        self.assertEqual(wires.air_wires[0].end_node.name, 'Y01_MiddleNode_1')
        self.assertEqual(wires.air_wires[0].end_node.x, 5.0)
        self.assertEqual(wires.air_wires[0].end_node.y, 0.0)
        self.assertEqual(wires.air_wires[0].end_node.z, 0.0)

        # 子线段2：起始坐标是子线段1的终止坐标，终止节点坐标是原线段的终止坐标
        self.assertEqual(wires.air_wires[1].start_node.name, 'Y01_MiddleNode_1')
        self.assertEqual(wires.air_wires[1].start_node.x, 5.0)
        self.assertEqual(wires.air_wires[1].start_node.y, 0.0)
        self.assertEqual(wires.air_wires[1].start_node.z, 0.0)
        self.assertEqual(wires.air_wires[1].end_node, node2)

        # 测试tubeWire的切分，应当被分为三段相等的tubeWire
        self.assertEqual(wires.tube_wires[0].sheath.start_node, node9)
        self.assertEqual(wires.tube_wires[0].sheath.end_node.z, 5)
        self.assertEqual(wires.tube_wires[2].sheath.end_node, node10)
        self.assertEqual(wires.tube_wires[0].core_wires[0].start_node, node11)
        self.assertEqual(wires.tube_wires[2].core_wires[0].end_node, node12)
        self.assertEqual(wires.tube_wires[0].core_wires[0].name, "Y11_Splited_1")
        self.assertEqual(wires.tube_wires[0].core_wires[0].end_node.name, "Y11_MiddleNode_1")
        self.assertEqual(wires.tube_wires[2].core_wires[0].name, "Y11_Splited_3")
        self.assertEqual(wires.tube_wires[2].core_wires[0].start_node.name, "Y11_MiddleNode_2")

    def test_Wires_get_parameters_matrix(self):
        # 初始化节点数据
        node1 = Node('X01', 0, 0, 10.5)
        node2 = Node('X02', 1000, 0, 10.5)
        node3 = Node('X03', 0, -0.4, 10)
        node4 = Node('X04', 1000, -0.4, 10)
        node5 = Node('X05', 0, 0.1, 10)
        node6 = Node('X06', 1000, 0.1, 10)
        node7 = Node('X07', 0, 0.6, 10)
        node8 = Node('X08', 1000, 0.6, 10)

        # 根据节点连接成线段
        wire1 = Wire('Y01', node1, node2, 0, 0.005, 0, 0, 58000000, 1, 1, [])
        wire2 = Wire('Y02', node3, node4, -0.4, 0.005, 0, 0, 58000000, 1, 1, [])
        wire3 = Wire('Y03', node5, node6, 0.1, 0.005, 0, 0, 58000000, 1, 1, [])
        wire4 = Wire('Y04', node7, node8, 0.6, 0.005, 0, 0, 58000000, 1, 1, [])

        # 创建线段集合
        wires = Wires()

        wires.add_air_wire(wire1)
        wires.add_air_wire(wire2)
        wires.add_ground_wire(wire3)
        wires.add_ground_wire(wire4)

        start_points = wires.get_start_points()
        end_points = wires.get_end_points()
        radii = wires.get_radii()
        offsets = wires.get_offsets()
        heights = wires.get_heights()
        lengths = wires.get_lengths()
        wires_num = wires.count()
        points_num = wires.count_distinct_points()
        index = wires.get_bran_index()

        expected_start_points = np.array([[0, 0, 10.5], [0, -0.4, 10], [0, 0.1, 10], [0, 0.6, 10]])
        expected_end_points = np.array([[1000, 0, 10.5], [1000, -0.4, 10], [1000, 0.1, 10], [1000, 0.6, 10]])
        expected_radii = np.array([[0.005], [0.005], [0.005], [0.005]])
        expected_offsets = np.array([[0], [-0.4], [0.1], [0.6]])
        expected_heights = np.array([[10.5], [10], [10], [10]])
        expected_lengths = np.array([[1000], [1000], [1000], [1000]])
        expected_wires_num = 4
        expected_points_num = 8
        expected_index = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])

        self.assertTrue(np.allclose(start_points, expected_start_points, rtol=1e-05))
        self.assertTrue(np.allclose(end_points, expected_end_points, rtol=1e-05))
        self.assertTrue(np.allclose(radii, expected_radii, rtol=1e-05))
        self.assertTrue(np.allclose(offsets, expected_offsets, rtol=1e-05))
        self.assertTrue(np.allclose(heights, expected_heights, rtol=1e-05))
        self.assertTrue(np.allclose(lengths, expected_lengths, rtol=1e-05))
        self.assertEqual(wires_num, expected_wires_num)
        self.assertEqual(points_num, expected_points_num)
        self.assertTrue(np.allclose(index, expected_index, rtol=1e-05))


class TestLightning(unittest.TestCase):
    def test_Lightning_init(self):
        # 创建一个8/20us的脉冲
        stroke1 = Stroke(stroke_type='CIGRE', duration=20e-6, is_calculated=True, parameter_set='8/20us')

        # 创建一个2.6/50us的脉冲
        stroke2 = Stroke(stroke_type='CIGRE', duration=50e-6, is_calculated=True, parameter_set='2.6/50us')

        stroke3 = Stroke(stroke_type='CIGRE', duration=10e-6, is_calculated=True, parameter_set=None, parameters=[0.25, 100, 6.4, 2, 0.9, 30, 0.5, 80, 2, 0.7])

        # 创建一个雷电对象,包含上面两个脉冲
        lightning = Lightning(1, "Direct", [stroke1])
        lightning.add_stroke(stroke2)
        lightning.add_stroke(stroke3)

        # 计算雷电在某个时间点的总波形
        time = 15e-6
        total_waveform = lightning.total_waveform(time)
        self.assertEqual(1.6999990164628942, total_waveform)


if __name__ == '__main__':
    unittest.main()
