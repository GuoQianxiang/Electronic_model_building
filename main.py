import numpy as np
from scipy.linalg import block_diag
from Model.Node import Node
from Model.Wires import Wire, Wires, CoreWire, TubeWire
from Model.Ground import Ground
from Model.Contant import Constant
from Model.Tower import Tower
from Utils.Math import calculate_wires_inductance_potential_with_ground
from Function.Calculators.Inductance import calculate_coreWires_inductance, calculate_sheath_inductance
from Function.Calculators.Capacitance import calculate_coreWires_capacitance, calculate_sheath_capacitance
from Function.Calculators.Impedance import calculate_coreWires_impedance, calculate_sheath_impedance, calculate_multual_impedance

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
    # 三条芯线的起点和终点
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
        # np.arange(100000, 1000000, 100000),
        # np.arange(1000000, 10000000, 1000000),
        # np.arange(10000000, 100000000, 10000000),
        # np.arange(100000000, 1000000000, 100000000)
    ])  # To be fixed later(when fre is too large, we can not calculate normally)
    VF = {'odc': 10,
          'frq': frq}
    f0 = 2e4
    max_length = 50

    # 根据节点连接成线段
    wire1 = Wire('Y01', node1, node2, 0, 0.005, 1, 0, 58000000, 1, 1, VF)
    wire2 = Wire('Y02', node2, node9, 0, 0.005, 1, 0, 58000000, 1, 1, VF)
    # 注意，空气和地面的线段不能相连、连接部分为a2g线段，后续添加一并处理
    wire3 = Wire('Y03', node4, node5, 0, 0.005, 1, 0, 58000000, 1, 1, VF)
    wire4 = Wire('Y04', node5, node6, 0, 0.005, 1, 0, 58000000, 1, 1, VF)

    # 创建套管线段集合
    core_wire1 = CoreWire("Y11", node11, node12, 0, 0.0087, 1, 0, 58000000, 1, 1, VF, 1.9, -5)
    core_wire2 = CoreWire("Y12", node13, node14, 0, 0.0087, 1, 0, 58000000, 1, 1, VF, 1.9, 0)
    core_wire3 = CoreWire("Y13", node15, node16, 0, 0.0087, 1, 0, 58000000, 1, 1, VF, 1.9, 5)
    sheath_wire = Wire("Y10", node9, node10, 0, 2, 1, 0, 1e7, 50, 1, VF)
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
    wires.add_tube_wire(tube_wire1)

    constants = Constant()
    # 对所有线段进行切分
    wires.display()
    wires.split_long_wires_all(max_length)
    # 将表皮线段添加到空气线段集合中
    for tubeWire in wires.tube_wires:
        wires.add_air_wire(tubeWire.sheath)  # sheath wire is in the air, we need to calculate it in air part.
    wires.display()
    # 初始化杆塔类
    tower = Tower(None, wires, None, ground, None, None, )
    # 计算空气中和地面线段的电感和电位系数
    L, P = calculate_wires_inductance_potential_with_ground(tower.wires, tower.ground, constants)

    Lc = calculate_coreWires_inductance(tube_wire1.get_coreWires_radii(), tube_wire1.get_coreWires_innerOffset(), tube_wire1.get_coreWires_innerAngle(), tube_wire1.sheath.r)
    print("Core wires inductance: ", Lc)

    Cc = calculate_coreWires_capacitance(tube_wire1.outer_radius, tube_wire1.inner_radius, tube_wire1.get_coreWires_epr(), Lc)
    print("Core wires capacitance: ", Cc)

    Ls = calculate_sheath_inductance(tube_wire1.get_coreWires_endNodeZ(), tube_wire1.sheath.r, tube_wire1.outer_radius)
    print("Sheath inductance: ", Ls)

    Cs = calculate_sheath_capacitance(tube_wire1.get_coreWires_endNodeZ(), tube_wire1.sheath.epr, Ls)
    print("Sheath capacitance: ", Cs)

    print("----------------------------------------------------------------")
    Zc = calculate_coreWires_impedance(tube_wire1.get_coreWires_radii(), tube_wire1.get_coreWires_innerOffset(), tube_wire1.get_coreWires_innerAngle(), tube_wire1.get_coreWires_mur(),
                                       tube_wire1.get_coreWires_sig(), tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, f0)
    print("Core wires impedance: ", Zc)

    Zs = calculate_sheath_impedance(tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, tube_wire1.sheath.r, f0)
    print("Sheath impedance: ", Zs)

    Zcs, Zsc = calculate_multual_impedance(tube_wire1.get_coreWires_radii(), tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, tube_wire1.sheath.r, f0)
    print("Multual impedance (Zcs): ", Zcs)
    print("Multual impedance (Zsc): ", Zsc)

    print("----------------------------------------------------------------")

    Zcf = calculate_coreWires_impedance(tube_wire1.get_coreWires_radii(), tube_wire1.get_coreWires_innerOffset(), tube_wire1.get_coreWires_innerAngle(), tube_wire1.get_coreWires_mur(),
                                       tube_wire1.get_coreWires_sig(), tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, VF["frq"])
    print("Frequency-dependent coreWires impedance (Zcf): ", Zcf)

    Zsf = calculate_sheath_impedance(tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, tube_wire1.sheath.r, VF["frq"])
    print("Frequency-dependent sheath impedance (Zsf): ", Zsf)

    Zcsf, Zscf = calculate_multual_impedance(tube_wire1.get_coreWires_radii(), tube_wire1.sheath.mur, tube_wire1.sheath.sig, tube_wire1.inner_radius, tube_wire1.sheath.r, VF["frq"])
    print("Frequency-dependent multual impedance(Zcsf): ", Zcsf)
    print("Frequency-dependent multual impedance(Zscf): ", Zscf)
    print("----------------------------------------------------------------")
    
    # 构成套管和芯线内部的阻抗矩阵，其中实部为电阻、虚部为电感，后续将会按照实部和虚部分别取出
    Zin = np.block([[Zs, Zsc],
                    [Zcs, Zc]])

    # 构成套管和芯线内部的电阻矩阵
    Rin = np.real(Zin) * max_length

    # 构成套管和芯线内部的电感矩阵
    Lin = (np.imag(Zin) / (2 * np.pi * f0) + block_diag(Ls, Lc)) * max_length

    # 构建套管和芯线内部的电容矩阵
    Cin = block_diag(Cs, Cc)

    # 计算套管和芯线的电感矩阵
    Lx = block_diag(0, (np.tile(np.imag(Zcs) / (2 * np.pi * f0), (1, 3)) + np.tile(np.imag(Zsc) / (2 * np.pi * f0), (3, 1))) * max_length)
    # 计算套管和芯线的电阻矩阵
    Rx = block_diag(0, (np.real(Zsc) + np.real(Zcs)) * max_length)

    # A矩阵
    print("------------------------------------------------")
    print("A matrix:")
    tower.initialize_incidence_matrix()
    print(tower.incidence_matrix)
    print("------------------------------------------------")

    # L矩阵
    print("------------------------------------------------")
    print("L matrix:")
    print(tower.inductance_matrix)
    tower.initialize_inductance_matrix()
    print(tower.inductance_matrix)
    tower.add_inductance_matrix(L)
    print(tower.inductance_matrix)
    tower.expand_inductance_matrix()
    print(tower.inductance_matrix)
    sheath_inductance_matrix = tower.update_inductance_matrix_by_coreWires()
    print(tower.inductance_matrix)
    tower.update_inductance_matrix_by_tubeWires(sheath_inductance_matrix, Lin, Lx)
    print(tower.inductance_matrix)
    print("------------------------------------------------")

    # R矩阵
    print("------------------------------------------------")
    print("R matrix:")
    print(tower.resistance_matrix)
    tower.initialize_resistance_matrix()
    print(tower.resistance_matrix)
    tower.expand_resistance_matrix()
    print(tower.resistance_matrix)
    tower.update_resistance_matrix_by_tubeWires(Rin, Rx)
    print(tower.resistance_matrix)
    print("------------------------------------------------")

    # P矩阵
    print("------------------------------------------------")
    print("P matrix")
    tower.initialize_potential_matrix()
    print(tower.potential_matrix)
    tower.add_potential_matrix(P)
    print(tower.potential_matrix)
    print("------------------------------------------------")

    # C矩阵
    print("------------------------------------------------")
    print("C matrix:")
    print(tower.capacitance_matrix)
    tower.initialize_capacitance_matrix()
    print(tower.capacitance_matrix)
    tower.update_capacitance_matrix_by_tubeWires(Cin)
    print(tower.capacitance_matrix)
    print("------------------------------------------------")
