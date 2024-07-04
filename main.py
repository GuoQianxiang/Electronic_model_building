import numpy as np
from Model.Node import Node
from Model.Wires import Wire, Wires
from Model.Ground import Ground
from Model.Contant import Constant
from Model.Tower import Tower
from Utils.Math import calculate_inductance, calculate_potential, calculate_wires_inductance_potential_with_ground


if __name__ == '__main__':
    # 初始化节点数据
    node1 = Node('X01', 0, 0, 10.5)
    node2 = Node('X02', 1000, 0, 10.5)
    node3 = Node('X03', 0, -0.4, 10)
    node4 = Node('X04', 1000, -0.4, 10)
    node5 = Node('X05', 0, 0.1, 10)
    node6 = Node('X06', 1000, 0.1, 10)
    node7 = Node('X07', 0, 0.6, 10)
    node8 = Node('X08', 1000, 0.6, 10)

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
    wire1 = Wire('Y01', node1, node2, 0, 0.005, 0.001, 1e-6, 58000000, 1, 1, VF)
    wire2 = Wire('Y02', node3, node4, -0.4, 0.005, 0.001, 1e-6, 58000000, 1, 1, VF)
    wire3 = Wire('Y03', node5, node6, 0.1, 0.005, 0.001, 1e-6, 58000000, 1, 1, VF)
    wire4 = Wire('Y04', node7, node8, 0.6, 0.005, 0.001, 1e-6, 58000000, 1, 1, VF)

    # 创建地面对象
    ground = Ground(1e-3, 1, 4, 'Lossy', 'weak', 'isolational')

    # 创建线段集合
    wires = Wires()

    wires.add_air_wire(wire1)
    wires.add_air_wire(wire2)
    wires.add_ground_wire(wire3)
    wires.add_ground_wire(wire4)


    constants = Constant()
    L, P = calculate_wires_inductance_potential_with_ground(wires, ground, constants)

    tower = Tower(None, wires, None, None, None, None,)
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
