import numpy as np


def Bessel_K2(z, n1, n2):
    """
    【函数功能】修正的第二类Bessel函数相除Kn-1(z)/Kn(z)近似表达
    【入参】
    z(float): Bessel函数变量
    n1(int): 分子的Bessel函数阶数
    n2(int): 分母的Bessel函数阶数

    【出参】
    K2(float): Kn-1(z)/Kn(z)近似表达
    """
    K2 = (1 + ((4 * n1 ** 2 - 1) / (8 * z)) + ((4 * n1 ** 2 - 1) * (4 * n1 ** 2 - 9) / (2 * (8 * z) ** 2)) + (
            (4 * n1 ** 2 - 1) * (4 * n1 ** 2 - 9) * (4 * n1 ** 2 - 25) / (6 * (8 * z) ** 3))) / (
                 1 + ((4 * n2 ** 2 - 1) / (8 * z)) + (
                 (4 * n2 ** 2 - 1) * (4 * n2 ** 2 - 9) / (2 * (8 * z) ** 2)) + (
                         (4 * n2 ** 2 - 1) * (4 * n2 ** 2 - 9) * (4 * n2 ** 2 - 25) / (6 * (8 * z) ** 3)))
    return K2


def Bessel_IK(z1, n1, z2, n2):
    """
    【函数功能】修正的第一类Bessel函数和第二类Bessel函数相乘，In1(z1)*Kn2(z2)近似表达
    【入参】
    z1(float): 第一类Bessel函数变量
    n1(int): 第一类BBessel函数阶数
    z2(float): 第二类Bessel函数变量
    n2(int): 第二类Bessel函数阶数

    【出参】
    IK(float): In1(z1)*Kn2(z2)近似表达
    """
    IK = np.exp(z1 - z2) / 2 / np.sqrt(z1 * z2) * (
            1 - ((4 * n1 ** 2 - 1) / (8 * z1)) + ((4 * n2 ** 2 - 1) / (8 * z2)) - ((4 * n1 ** 2 - 1) / (8 * z1)) * (
            (4 * n2 ** 2 - 1) / (8 * z2)))
    return IK


def calculate_distances(points1, points2):
    """
    计算两个 n x 3 矩阵中对应行之间的距离.
    
    参数:
    points1 (np.ndarray): 第一个 n x 3 矩阵,每行表示一个点的 x, y, z 坐标
    points2 (np.ndarray): 第二个 n x 3 矩阵,每行表示一个点的 x, y, z 坐标
    
    返回:
    np.ndarray: 一个 n x 1 矩阵,表示两个矩阵中对应行之间的距离
    """
    if points1.shape != points2.shape:
        raise ValueError("两个输入矩阵必须有相同的形状!")
    
    distances = np.zeros((points1.shape[0], 1))
    for i in range(points1.shape[0]):
        distances[i] = np.sum((points1[i] - points2[i])**2)
    
    return distances


def calculate_direction_cosines(start_points, end_points, lengths):
    """
    计算 x、y 和 z 方向上的余弦值矩阵。

    参数:
    start_points (numpy.ndarray): n*3 矩阵,表示 n 条线段的起点坐标(x, y, z)
    end_points (numpy.ndarray): n*3 矩阵,表示 n 条线段的终点坐标(x, y, z)
    lengths (numpy.ndarray): n*1 矩阵,表示 n 条线段的长度

    返回:
    x_cosines, y_cosines, z_cosines(numpy.ndarray, numpy.ndarray, numpy.ndarray): x、y 和 z 方向上的余弦值矩阵
    """
    # 计算 x 方向上的余弦值
    x_cosines = (end_points[:, 0] - start_points[:, 0]).reshape(lengths.shape[0], 1) / lengths

    # 计算 y 方向上的余弦值
    y_cosines = (end_points[:, 1] - start_points[:, 1]).reshape(lengths.shape[0], 1) / lengths

    # 计算 z 方向上的余弦值
    z_cosines = (end_points[:, 2] - start_points[:, 2]).reshape(lengths.shape[0], 1) / lengths

    return x_cosines, y_cosines, z_cosines