import numpy as np
from Model.Node import Node
from Model.Wires import Wire, Wires, CoreWire, TubeWire
from Model.Ground import Ground
from Model.Contant import Constant
from Model.Tower import Tower
from Utils.Math import calculate_inductance, calculate_potential, calculate_wires_inductance_potential_with_ground


if __name__ == '__main__':
    # 初始化节点数据
    node1 = Node('X01', 0, -0.4, 10)
    node2 = Node('X02', 0, -0.4, 9.8)
    node3 = Node('X03', 0, 0.1, 10)
    node4 = Node('X04', 0, 0.1, -1)
    node5 = Node('X05', 0, 0.6, -1)
    node6 = Node('X06', 0, 0.7, -1)
    node7 = Node('X07', 0, -0.4, 9.8)
    node8 = Node('X08', 0, 0, 9.8)
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
    wire2 = Wire('Y02', node2, node3, 0, 0.005, 0, 0, 58000000, 1, 1, VF)
    # 注意，空气和地面的线段不能相连、连接部分为a2g线段，后续添加一并处理
    wire3 = Wire('Y03', node4, node5, 0, 0.005, 0, 0, 58000000, 1, 1, VF)
    wire4 = Wire('Y04', node5, node6, 0, 0.005, 0, 0, 58000000, 1, 1, VF)

    # 创建套管线段集合
    core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, -5)
    core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 0)
    core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 0, 0, 58000000, 1, 1, VF, 1.9, 5)
    sheath_wire = Wire("Y10", node9, node10, 0, 2, 0, 0, 1e7, 50, 1, VF)
    tube_wire1 = TubeWire(sheath_wire, 2.05, 2.1, 3)
    tube_wire1.add_core_wire(core_wire1)
    tube_wire1.add_core_wire(core_wire2)
    tube_wire1.add_core_wire(core_wire3)

    # 创建地面对象
    ground = Ground(1e-3, 1, 4, 'Lossy', 'weak', 'isolational')

    # 创建线段集合
    wires = Wires()

    wires.add_air_wire(wire1)
    wires.add_air_wire(wire2)
    wires.add_ground_wire(wire3)
    wires.add_ground_wire(wire4)
    # wires.add_tube_wire(tube_wire1)


    constants = Constant()

    tower = Tower(None, wires, None, None, None, None,)
    L, P = calculate_wires_inductance_potential_with_ground(tower.wires, ground, constants)
    # A矩阵
    print("------------------------------------------------")
    print("A matrix:")
    tower.initialize_incidence_matrix()
    print(tower.incidence_matrix)
    print("------------------------------------------------")

    # L矩阵
    print("------------------------------------------------")
    print("L matrix:")
    tower.initialize_inductance_matrix()
    print(tower.inductance_matrix)
    tower.update_inductance_matrix(L)
    print(tower.inductance_matrix)
    print("------------------------------------------------")

    # R矩阵
    print("------------------------------------------------")
    print("R matrix:")
    tower.initialize_resistance_matrix()
    print(tower.resistance_matrix)
    print("------------------------------------------------")

    # P矩阵
    print("------------------------------------------------")
    print("P matrix")
    tower.initialize_potential_matrix()
    print(tower.potential_matrix)
    tower.update_potential_matrix(P)
    print(tower.potential_matrix)
    print("------------------------------------------------")