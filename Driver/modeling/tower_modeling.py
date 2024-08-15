import numpy as np
from Function.Calculators.Inductance import calculate_coreWires_inductance, calculate_sheath_inductance, calculate_wires_inductance_potential_with_ground
from Function.Calculators.Capacitance import calculate_coreWires_capacitance, calculate_sheath_capacitance
from Function.Calculators.Impedance import calculate_coreWires_impedance, calculate_sheath_impedance, calculate_multual_impedance
from Model.Contant import Constant
from scipy.linalg import block_diag


def build_incidence_matrix(tower):
    # A矩阵
    print("------------------------------------------------")
    print("A matrix is building...")

    tower.initialize_incidence_matrix()

    print(tower.incidence_matrix)
    print("A matrix is built successfully")
    print("------------------------------------------------")


def build_resistance_matrix(tower, Rin, Rx):
    # R矩阵
    print("------------------------------------------------")
    print("R matrix is building...")

    tower.initialize_resistance_matrix()

    tower.expand_resistance_matrix()

    tower.update_resistance_matrix_by_tubeWires(Rin, Rx)

    print(tower.resistance_matrix)
    print("R matrix is built successfully")
    print("------------------------------------------------")


def build_inductance_matrix(tower, L, Lin, Lx):
    # L矩阵
    print("------------------------------------------------")
    print("L matrix is building...")

    tower.initialize_inductance_matrix()

    tower.add_inductance_matrix(L)

    tower.expand_inductance_matrix()

    sheath_inductance_matrix = tower.update_inductance_matrix_by_coreWires()

    tower.update_inductance_matrix_by_tubeWires(sheath_inductance_matrix, Lin, Lx)

    print(tower.inductance_matrix)
    print("L matrix is built successfully")
    print("------------------------------------------------")


def build_potential_matrix(tower, P):
    # P矩阵
    print("------------------------------------------------")
    print("P matrix is building...")

    tower.initialize_potential_matrix()

    tower.add_potential_matrix(P)

    print(tower.potential_matrix)
    print("P matrix is built successfully")
    print("------------------------------------------------")


def build_capacitance_matrix(tower, Cin):
    # C矩阵
    print("------------------------------------------------")
    print("C matrix is building...")

    tower.initialize_capacitance_matrix()

    tower.update_capacitance_matrix_by_tubeWires(Cin)

    print(tower.capacitance_matrix)
    print("C matrix is built successfully")
    print("------------------------------------------------")


def build_impedance_matrix(tubeWire, frequency):
    # 计算套管和芯线内部的阻抗矩阵
    # Core wires impedance
    Zc = calculate_coreWires_impedance(tubeWire.get_coreWires_radii(), tubeWire.get_coreWires_innerOffset(), tubeWire.get_coreWires_innerAngle(), tubeWire.get_coreWires_mur(),
                                       tubeWire.get_coreWires_sig(), tubeWire.sheath.mur, tubeWire.sheath.sig, tubeWire.inner_radius, frequency)

    # Sheath impedance
    Zs = calculate_sheath_impedance(tubeWire.sheath.mur, tubeWire.sheath.sig, tubeWire.inner_radius, tubeWire.sheath.r, frequency)

    # Multual impedance
    Zcs, Zsc = calculate_multual_impedance(tubeWire.get_coreWires_radii(), tubeWire.sheath.mur, tubeWire.sheath.sig, tubeWire.inner_radius, tubeWire.sheath.r, frequency)
    
    # 构成套管和芯线内部的阻抗矩阵，其中实部为电阻、虚部为电感，后续将会按照实部和虚部分别取出
    Zin = np.block([[Zs, Zsc],
                    [Zcs, Zc]])
    return Zin, Zcs, Zsc


def build_tubeWire_inductance_capacitance(tubeWire):
    # Core wires inductance
    Lc = calculate_coreWires_inductance(tubeWire.get_coreWires_radii(), tubeWire.get_coreWires_innerOffset(), tubeWire.get_coreWires_innerAngle(), tubeWire.sheath.r)

    # Core wires capacitance
    Cc = calculate_coreWires_capacitance(tubeWire.outer_radius, tubeWire.inner_radius, tubeWire.get_coreWires_epr(), Lc)

    # Sheath inductance
    Ls = calculate_sheath_inductance(tubeWire.get_coreWires_endNodeZ(), tubeWire.sheath.r, tubeWire.outer_radius)

    # Sheath capacitance
    Cs = calculate_sheath_capacitance(tubeWire.get_coreWires_endNodeZ(), tubeWire.sheath.epr, Ls)

    return Lc, Cc, Ls, Cs


def prepare_building_parameters(tubeWire, max_length, frequency):
    Zin, Zcs, Zsc = build_impedance_matrix(tubeWire, frequency)
    Lc, Cc, Ls, Cs = build_tubeWire_inductance_capacitance(tubeWire)
    # 构成套管和芯线内部的电阻矩阵
    Rin = np.real(Zin) * max_length

    # 构成套管和芯线内部的电感矩阵
    Lin = (np.imag(Zin) / (2 * np.pi * frequency) + block_diag(Ls, Lc)) * max_length

    # 构建套管和芯线内部的电容矩阵
    Cin = block_diag(Cs, Cc)

    # 计算套管和芯线的电感矩阵
    Lx = block_diag(0, (np.tile(np.imag(Zcs) / (2 * np.pi * frequency), (1, 3)) + np.tile(np.imag(Zsc) / (2 * np.pi * frequency), (3, 1))) * max_length)
    # 计算套管和芯线的电阻矩阵
    Rx = block_diag(0, (np.real(Zsc) + np.real(Zcs)) * max_length)

    return Rin, Rx, Lin, Lx, Cin


def tower_building(tower, frequency, max_length):
    print("------------------------------------------------")
    print("Tower building...")
    # 0.参数准备
    constants = Constant()
    Rin, Rx, Lin, Lx, Cin = prepare_building_parameters(tower.tubeWire, max_length, frequency)
    L, P = calculate_wires_inductance_potential_with_ground(tower.wires, tower.ground, constants)

    # 1. 构建A矩阵
    build_incidence_matrix(tower)

    # 2. 构建R矩阵
    build_resistance_matrix(tower, Rin, Rx)

    # 3. 构建L矩阵
    build_inductance_matrix(tower, L, Lin, Lx)

    # 4. 构建P矩阵
    build_potential_matrix(tower, P)

    # 5. 构建C矩阵
    build_capacitance_matrix(tower, Cin)
    print("Tower building is completed.")
    print("------------------------------------------------")