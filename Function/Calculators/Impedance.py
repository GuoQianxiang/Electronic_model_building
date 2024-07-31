import sys

sys.path.append('../..')
import numpy as np
from scipy.special import iv as besseli
from scipy.special import kv as besselk
from Utils.Math import Bessel_IK, Bessel_K2

def calculate_coreWires_impedance(core_wires_r, core_wires_offset, core_wires_angle, core_wires_mur,
                                  core_wires_sig, sheath_mur, sheath_sig, sheath_inner_radius, Frq):
    """
    【函数功能】芯线阻抗计算
    【入参】
    core_wires_r (numpy.ndarray, n*1): n条芯线的半径
    core_wires_offset (numpy.ndarray, n*1): n条芯线距离中心位置
    core_wires_angle (numpy.ndarray, n*1): n条芯线角度
    core_wires_mur (numpy.ndarray, n*1): n条芯线的磁导率
    core_wires_sig (numpy.ndarray, n*1): n条芯线的电导率
    sheath_mur (float): 套管的磁导率
    sheath_sig (float): 套管的电导率
    sheath_inner_radius (float): 套管的内径
    Frq(numpy.ndarray,1*Nf):Nf个频率组成的频率矩阵

    【出参】
    Zc(numpy.ndarray:n*n*Nf): n条芯线在Nf个频率下的阻抗矩阵
    """
    mu0 = 4 * np.pi * 1e-7
    ep0 = 8.854187818e-12
    Besl_Max = 200
    Nbesl = 15
    frq = np.array([Frq]).reshape(-1)
    Npha = core_wires_r.shape[0]
    Mu_c = mu0 * core_wires_mur[0]
    Mu_s = mu0 * sheath_mur
    Nf = frq.size
    omega = 2 * np.pi * frq
    gamma_c = np.sqrt(1j * Mu_c * omega * (core_wires_sig[0] + 1j * omega * ep0))
    gamma_s = np.sqrt(1j * Mu_s * omega * (sheath_sig + 1j * omega * ep0))
    Rsa = sheath_inner_radius * gamma_s
    Zc_diag = 1 / (2 * np.pi * core_wires_r * core_wires_sig[0]) * gamma_c
    Rc = core_wires_r * gamma_c
    kc = 1 / (2 * np.pi * core_wires_r) * (1j * omega * Mu_c / gamma_c)
    low = np.where(np.real(Rc) <= Besl_Max)
    Zc_diag[low] = kc[low] * besseli(0, Rc[low]) / besseli(1, Rc[low])
    Nc = core_wires_r.shape[0]
    Zc = np.zeros((Nc, Nc, Nf), dtype='complex')
    for ik in range(Nf):
        Zc[:, :, ik] = np.diag(Zc_diag[:, ik])

    tmat = np.tile(core_wires_angle, (1, Npha))
    angle = (tmat - tmat.T) * np.pi / 180
    didk = core_wires_offset * core_wires_offset.T
    KR = np.zeros((Nbesl, Nf), dtype='complex')
    for ik in range(Nbesl):
        KR[ik, :] = Bessel_K2(Rsa, ik, ik + 1)
        low = np.where(np.real(Rsa) <= Besl_Max)
        KR[ik, low] = besselk(ik, Rsa[low]) / besselk(ik + 1, Rsa[low])

    ks = 1j * omega * Mu_s / (2 * np.pi)
    for jk in range(Nf):
        K0 = ks[jk] * KR[0, jk] / Rsa[jk]
        Zc[:, :, jk] += K0

    Kt = 0
    Ktmp = np.zeros((Npha, Npha, Nf), dtype='complex')
    Km = np.zeros((Nbesl, Nf), dtype='complex')
    for ik in range(Nbesl):
        Km[ik, :] = ks * (2 / ((ik + 1) * (1 + sheath_mur) + Rsa * KR[ik, :]))
        Kn = (didk / (sheath_inner_radius * sheath_inner_radius)) ** (ik + 1) * np.cos((ik + 1) * angle)
        for jk in range(Nf):
            Ktmp[:, :, jk] = Kn * Km[ik, jk]
        Kt += Ktmp
    Zc += Kt
    # process the data, because the Z matrix is 3-dimensional matrix, but when fre is a float, we need Z is a 2-dimensional array
    if isinstance(Frq, float):
        Zc = np.squeeze(Zc)
    return Zc


def calculate_sheath_impedance(sheath_mur, sheath_sig, sheath_inner_radius, sheath_r, Frq):
    """
    【函数功能】套管阻抗计算
    【入参】
    sheath_mur (float): 套管的磁导率
    sheath_sig (float): 套管的电导率
    sheath_inner_radius (float): 套管的内径
    sheath_r (float): 套管的外径
    Frq(numpy.ndarray,1*Nf):Nf个频率组成的频率矩阵

    【出参】
    Zs(numpy.ndarray:1*1*Nf): Nf个频率下的套管阻抗矩阵
    """
    mu0 = 4 * np.pi * 1e-7
    ep0 = 8.854187818e-12
    Besl_Max = 200
    frq = np.array([Frq]).reshape(-1)
    Mu_s = mu0 * sheath_mur
    Nf = frq.size
    omega = 2 * np.pi * frq
    gamma_s = np.sqrt(1j * Mu_s * omega * (sheath_sig + 1j * omega * ep0))
    Rsa = sheath_inner_radius * gamma_s
    Rsb = sheath_r * gamma_s
    ks = 1j * omega * Mu_s / (2 * np.pi * Rsb)
    Zs_diag = np.copy(ks)

    dR = Rsb - Rsa
    low = np.where(np.real(dR) <= Besl_Max)
    Zs_diag[low] = ks[low] * np.cosh(dR[low]) / np.sinh(dR[low])

    low = np.where(np.real(Rsb) <= Besl_Max)
    tmp1 = besseli(0, Rsb[low]) * besselk(1, Rsa[low]) + besseli(1, Rsa[low]) * besselk(0, Rsb[low])
    tmp2 = besseli(1, Rsb[low]) * besselk(1, Rsa[low]) - besseli(1, Rsa[low]) * besselk(1, Rsb[low])
    Zs_diag[low] = ks[low] * tmp1 / tmp2

    Ns = np.array([sheath_sig]).reshape(-1).shape[0]
    Zs = np.zeros((Ns, 1, Nf), dtype='complex')
    for ik in range(Nf):
        Zs[:, 0, ik] = Zs_diag[ik]
    # process the data, because the Z matrix is 3-dimensional matrix, but when fre is a float, we need Z is a 2-dimensional array
    if isinstance(Frq, float):
        Zs = np.squeeze(Zs)
    return Zs


def calculate_multual_impedance(core_wires_r, sheath_mur, sheath_sig, sheath_inner_radius, sheath_r, Frq):
    """
    【函数功能】互阻抗计算
    【入参】
    core_wires_r (numpy.ndarray, n*1): n条芯线的半径
    sheath_mur (float): 套管的磁导率
    sheath_sig (float): 套管的电导率
    sheath_inner_radius (float): 套管的内径
    sheath_r (float): 套管的外径
    Frq(numpy.ndarray,1*Nf):Nf个频率组成的频率矩阵

    【出参】
    Zcs(numpy.ndarray:n*1*Nf): Nf个频率下的芯线和表皮之间的互阻抗矩阵, n为芯线数量
    Zsc(numpy.ndarray:1*n*Nf): Nf个频率下的表皮和芯线之间的互阻抗矩阵, n为芯线数量
    """
    mu0 = 4 * np.pi * 1e-7
    ep0 = 8.854187818e-12
    Besl_Max = 200
    frq = np.array([Frq]).reshape(-1)
    # Npha 表示芯线数量
    Npha = core_wires_r.shape[0]
    Mu_s = mu0 * sheath_mur
    Nf = frq.size
    omega = 2 * np.pi * frq
    gamma_s = np.sqrt(1j * Mu_s * omega * (sheath_sig + 1j * omega * ep0))
    Rsa = sheath_inner_radius * gamma_s
    Rsb = sheath_r * gamma_s
    ks = 1j * omega * Mu_s / (2 * np.pi * Rsa * Rsb)
    Z0 = ks * np.zeros(Nf, dtype='complex')

    dR = Rsb - Rsa
    low = np.where(np.real(dR) <= Besl_Max)
    Itmp1 = Bessel_IK(Rsa[low], 1, Rsb[low], 1) - Bessel_IK(Rsb[low], 1, Rsa[low], 1)
    Z0[low] = ks[low] / Itmp1

    low = np.where(np.real(Rsb) <= Besl_Max)
    Itmp2 = besseli(1, Rsa[low]) * besselk(1, Rsb[low]) - besseli(1, Rsb[low]) * besselk(1, Rsa[low])
    Z0[low] = ks[low] / Itmp2

    Zcs = np.zeros((Npha, 1, Nf), dtype='complex')
    Zsc = np.zeros((1, Npha, Nf), dtype='complex')
    for ik in range(Nf):
        Zcs[:, 0, ik] = Z0[ik]
        Zsc[0, :, ik] = Z0[ik]
    # process the data, because the Z matrix is 3-dimensional matrix, but when fre is a float, we need Z is a 2-dimensional array
    if isinstance(Frq, float):
        Zsc = np.squeeze(Zsc) # Zsc should be 1*n
        Zcs = np.squeeze(Zcs).reshape(-1, 1) # Zcs should be n*1

    return Zcs, Zsc


def calculate_ground_impedance(ground_mur, ground_epr, ground_sig, end_node_z, sheath_outer_radius, Dist, Frq):
    """
    【函数功能】地阻抗计算
    【入参】
    ground_mur(float):大地相对磁导率
    ground_epr(float):大地相对介电常数
    ground_sig(float):大地电导率
    end_node_z (numpy.ndarray,n*1): n条芯线的第二个节点的z值
    sheath_outer_radius (float): 整体外径
    Dist:未知
    Frq(numpy.ndarray,1*Nf):Nf个频率组成的频率矩阵

    【出参】
    Zg(numpy.ndarray:1*1*Nf): Nf个频率下的地阻抗矩阵
    """
    mu0 = 4 * np.pi * 1e-7
    ep0 = 8.854187818e-12
    Mur_g = ground_mur * mu0
    Epr_g = ground_epr * ep0
    frq = np.array([Frq]).reshape(-1)
    r0 = np.array([sheath_outer_radius]).reshape(-1)
    Ncon = r0.size
    Nf = frq.size
    Zg = np.zeros((Ncon, Ncon, Nf), dtype='complex')

    omega = 2 * np.pi * frq
    gamma = np.sqrt(1j * Mur_g * omega * (ground_sig + 1j * omega * Epr_g))
    km = 1j * omega * Mur_g / 4 / np.pi

    if end_node_z[0] > 0 and end_node_z[0] < 1e6:
        for i1 in range(Ncon):
            for i2 in range(Ncon - i1):
                d = abs(Dist[i1] - Dist[i2 + i1])
                h1 = end_node_z[0][i1]
                h2 = end_node_z[0][i2 + i1]
                Zg[i1, i2 + i1, :] = km * np.log(((1 + gamma * (h1 + h2) / 2) ** 2 + (d * gamma / 2) ** 2) / (
                        (gamma * (h1 + h2) / 2) ** 2 + (d * gamma / 2) ** 2))
                Zg[i2 + i1, i1, :] = np.copy(Zg[i1, i2 + i1, :])

        for i in range(Ncon):
            h = end_node_z[0][i]
            Zg[i, i, :] = km * np.log(((1 + gamma * h) ** 2) / ((gamma * h) ** 2))

    elif end_node_z[0] < 0:
        for i1 in range(Ncon):
            R0 = r0 * gamma
            Zg[i1, i1, :] = 2 * km * np.log((1 + R0) / R0)

    return Zg