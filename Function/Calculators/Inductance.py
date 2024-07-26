import numpy as np


def calculate_coreWires_inductance(core_wires_r, core_wires_offset, core_wires_angle, sheath_inner_radius):
    """
    【函数功能】芯线电感计算
    【入参】
    core_wires_r (numpy.ndarray, n*1): n条芯线的半径
    core_wires_offset (numpy.ndarray, n*1): n条芯线距离中心位置
    core_wires_angle (numpy.ndarray, n*1): n条芯线角度
    sheath_inner_radius (float): 套管的内径

    【出参】
    Lc(numpy.ndarray:n*n): n条芯线电感矩阵
    """
    mu0 = 4 * np.pi * 1e-7
    Npha = core_wires_r.shape[0]
    tmat = np.tile(core_wires_angle, (1, Npha)) # tmat is
    cost = np.cos((tmat - tmat.T) * np.pi / 180)
    didk = core_wires_offset.dot(core_wires_offset.T)
    tmp0 = core_wires_offset * core_wires_offset
    tmat = np.tile(tmp0, (1, Npha))
    di2dk2 = tmat + tmat.T
    tmp1 = didk ** 2 + sheath_inner_radius ** 4 - 2 * didk * cost * sheath_inner_radius ** 2
    tmp2 = di2dk2 - 2 * didk * cost
    tmp0 = np.sqrt(tmp1 / tmp2)
    Lc = mu0 / (2 * np.pi) * np.log(tmp0 / sheath_inner_radius)
    Lc_diag = mu0 / (2 * np.pi) * np.log(
        (sheath_inner_radius * sheath_inner_radius - core_wires_offset * core_wires_offset) / (core_wires_r * sheath_inner_radius))
    np.fill_diagonal(Lc, Lc_diag)
    return Lc


def calculate_sheath_inductance(end_node_z, sheath_r, sheath_outer_radius):
    """
    【函数功能】套管电感计算
    【入参】
    end_node_z (numpy.ndarray,n*1): n条芯线的第二个节点的z值
    sheath_r (float): 套管的外径
    sheath_outer_radius (float): 套管整体外径

    【出参】
    Ls(float)：套管电感
    """
    mu0 = 4 * np.pi * 1e-7
    Vduct = 1e6
    if end_node_z[0] >= Vduct:
        Ls = 0
    elif end_node_z[0] > 0:
        Ls = mu0 / (2 * np.pi) * np.log(2 * end_node_z[0] / sheath_r)
    elif end_node_z[0] == 0:
        Ls = mu0(2 * np.pi) * np.log(2 * (2 * sheath_outer_radius) / sheath_r)
    elif end_node_z[0] < 0:
        Ls = mu0 / (2 * np.pi) * np.log(sheath_outer_radius / sheath_r)
    else:
        Ls = 0
    return Ls