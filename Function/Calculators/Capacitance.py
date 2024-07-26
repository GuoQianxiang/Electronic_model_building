import numpy as np


def calculate_coreWires_capacitance(sheath_outer_radius, sheath_inner_radius, core_wires_epr, Lc):
    """
    【函数功能】芯线电容计算
    【入参】
    sheath_inner_radius (float): 套管的内径
    sheath_outer_radius (float): 套管的整体外径
    core_wires_epr (numpy.ndarray, n*1): n条芯线的相对介电常数
    Lc(numpy.ndarray:n*n): n条芯线的电感矩阵

    【出参】
    Cc(numpy.ndarray:n*n): n条芯线电容矩阵
    """
    V0 = 3e8
    if sheath_outer_radius / sheath_inner_radius < 10:
        Vc = V0 / np.sqrt(core_wires_epr[0])
    else:
        Vc = V0
    Cc = np.linalg.inv(Lc) / Vc ** 2
    return Cc


def calculate_sheath_capacitance(end_node_z, sheath_epr, Ls):
    """
    【函数功能】套管电容计算
    【入参】
    end_node_z (numpy.ndarray,n*1): n条芯线的第二个节点的z值
    sheath_epr (float): 套管的相对介电常数
    Ls(float)：套管电感

    【出参】
    Cs(float)：套管电容
    """
    V0 = 3e8
    Vduct = 1e6
    if end_node_z[0] >= Vduct:
        Cs = 0
    elif end_node_z[0] > 0:
        Cs = 1 / (Ls * V0 ** 2)
    elif end_node_z[0] == 0:
        Cs = 1 / (Ls * V0 ** 2)
    elif end_node_z[0] < 0:
        Vs = V0 / np.sqrt(sheath_epr)
        Cs = 1 / (Ls * Vs ** 2)
    else:
        Cs = 0
    return Cs