import math
import numpy as np
import numpy.matlib
from Model.Wires import Wires


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


def expand_matrix(matrix, i, end, m):
    """
    从矩阵中取出第i行和第i列,并将其复制m次扩充成(n+m)*(n+m)的矩阵
    
    参数:
    matrix (numpy.ndarray): 输入矩阵
    i (int): 要取出的行和列索引
    end (int): 要取出的行列的截止位置和赋值的截止位置(保证在循环过程中不会取出多余的部分)
    m (int): 复制的次数
    
    返回:
    expanded_matrix (numpy.ndarray): 扩充后的矩阵
    """
    n = matrix.shape[0]  # 获取原始矩阵的大小
    
    # 创建一个全零矩阵,大小为(n+m)*(n+m)
    expanded_matrix = np.zeros((n+m, n+m), dtype=matrix.dtype)
    
    # 将原始矩阵复制到新矩阵的左上角
    expanded_matrix[:n, :n] = matrix
    
    # 将第i行复制到新矩阵的最后m行
    expanded_matrix[n:, :end] = np.tile(matrix[i, :end], (m, 1))
    
    # 将第i列复制到新矩阵的最后m列
    expanded_matrix[:end, n:] = np.tile(matrix[:end, i][:, np.newaxis], (1, m))
    
    return expanded_matrix


def copy_and_expand_matrix(original_matrix, m):
    """
    将一个n*n的矩阵扩展为一个mn*mn的矩阵,其中主对角线上的m*m矩阵块为0,
    其余的m*m矩阵块按照原先n*n的矩阵对应位置的数值复制填充。

    参数:
    original_matrix (numpy.ndarray): 输入n*n的矩阵
    m (int): 每个子矩阵块的大小

    返回:
    expanded_matrix (numpy.ndarray): 扩展后的mn*mn矩阵
    """
    n = original_matrix.shape[0]  # 原始矩阵的大小
    expanded_size = n * m  # 扩展后矩阵的大小

    # 创建一个全零的扩展矩阵
    expanded_matrix = np.zeros((expanded_size, expanded_size), dtype=original_matrix.dtype)

    # 遍历原始矩阵的每个元素
    for i in range(n):
        for j in range(n):
            # 计算子矩阵块的起始位置
            row_start = i * m
            col_start = j * m

            # 将当前元素复制为m*m的子矩阵块
            expanded_matrix[row_start:row_start+m, col_start:col_start+m] = np.full((m, m), original_matrix[i, j])

            # 将主对角线上的m*m矩阵块设置为0
            if i == j:
                expanded_matrix[row_start:row_start+m, col_start:col_start+m] = 0

    return expanded_matrix


def update_matrix(matrix, indices, submatrix):
    """
    将 n*n 的 NumPy 矩阵中,指定的行列索引对应的区域,替换为 m*m 的子矩阵。

    参数:
    matrix (numpy.ndarray): 输入的 n*n 矩阵
    indices (list): 长度为 m*m 的列表,表示要替换的行列索引
    submatrix (numpy.ndarray): 要替换的 m*m 子矩阵

    返回:
    updated_matrix (numpy.ndarray): 更新后的 n*n 矩阵
    """
    n = matrix.shape[0]

    updated_matrix = matrix.copy()  # 创建输入矩阵的副本
    i = 0
    for index in indices:
        updated_matrix[index, indices] = submatrix[i, :]
        i += 1

    return updated_matrix


def Cal_LC_OHL(High, Dist, r0):
    """
    【函数功能】计算线段集的互感矩阵和互容矩阵
    【入参】
    High(numpy.ndarray: n*1): n条线的高度
    Dist(numpy.ndarray: n*1): n条线的偏置
    r0(numpy.ndarray: n*1): n条线的半径

    【出参】
    L(numpy.ndarray: n*n): n条导线的互感矩阵
    C(numpy.ndarray: n*n): n条导线的互容矩阵
    """
    # Calculate OHL Parameters (L and C per unit) with Height and hori. Dist
    # 此处的High、Dist、r0都是list，而非矩阵，由于输入是n*1的矩阵，所以需要做flatten操作
    High = High.flatten()
    Dist = Dist.flatten()
    r0 = r0.flatten()
    Vair = 3e8  # Velocity in free space
    mu0 = 4 * math.pi * 1e-7
    km = mu0 / (2 * math.pi)
    Ncon = High.shape[0]
    # 计算自己对自己的电感，是一个对角矩阵
    out = np.log(2 * High / r0)
    L = np.diag(out)
    L = L.copy()  

    for i1 in range(Ncon - 1):
        for i2 in range(i1 + 1, Ncon):
            d = np.abs(Dist[i1] - Dist[i2])
            h1 = High[i1]
            h2 = High[i2]
            L[i1, i2] = 0.5 * np.log((d ** 2 + (h1 + h2) ** 2) / (d ** 2 + (h1 - h2) ** 2))
            L[i2, i1] = L[i1, i2] # 两两互换位置，相对互感相同，因此是对称对角矩阵

    L = km * L
    C = np.linalg.inv(L) / Vair ** 2

    return L, C


def INT_LINE_D2P_D(U1a, U1b, V1, W1, r1, U2a, U2b, V2, W2, r2):

        # (0) initialization
        ELIM = 1e-9  # limit for changing formula
        a2 = np.maximum(r2, r1)  # avoiding log(0) for negative uij
        a2 = a2 * a2

        no = len(U1a)
        ns = len(U2a)

        if no != ns:
            out = []
            return out

        u13 = U1a - U2a
        u14 = U1a - U2b
        u23 = U1b - U2a
        u24 = U1b - U2b

        u13s = u13 * u13
        u23s = u23 * u23
        u14s = u14 * u14
        u24s = u24 * u24

        As = (V2 - V1) * (V2 - V1) + (W2 - W1) * (W2 - W1)
        As = np.maximum(As, a2)
        t132 = np.array(As + u13s, dtype=float)
        t232 = np.array(As + u23s, dtype=float)
        t142 = np.array(As + u14s, dtype=float)
        t242 = np.array(As + u24s, dtype=float)

        t13 = np.sqrt(t132)
        t23 = np.sqrt(t232)
        t14 = np.sqrt(t142)
        t24 = np.sqrt(t242)

        # using the exact formulas for calculation
        a = -u24 * np.log(u24 + t24)
        b = - u13 * np.log(u13 + t13)
        c = u23 * np.log(u23 + t23)
        d = u14 * np.log(u14 + t14)
        I1 = -u24 * np.log(u24 + t24) - u13 * np.log(u13 + t13) + u23 * np.log(u23 + t23) + u14 * np.log(u14 + t14)

        s = u24 + t24
        Idex = s < ELIM
        s = u13 + t13
        s = u23 + t23
        s = u14 + t14

        if np.sum(Idex) != 0:
            I1a = u24 * np.log(t24 - u24) + u13 * np.log(t13 - u13) - u23 * np.log(t23 - u23) - u14 * np.log(
                t14 - u14)
            I1[Idex] = I1a[Idex]

        I2 = t24 + t13 - t23 - t14
        out = I1 + I2

        return out


def calculate_inductance(ps1, ps2, rs, pf1, pf2, rf):
    """
    【函数功能】计算线段集的电感矩阵
    【入参】
    ps1(numpy.ndarray: n*3): n条线的起始点坐标
    ps2(numpy.ndarray: n*3): n条线的终止点坐标
    rs(numpy.ndarray: n*1): n条线的半径

    【出参】
    INT(numpy.ndarray: n*n): n条线段的电感矩阵
    """
    PROD_MOD = 2  # matrix product
    COEF_MOD = 2  # inductance
    return INT_SLAN_2D(ps1, ps2, rs, pf1, pf2, rf, PROD_MOD, COEF_MOD)


def INT_SLAN_2D(ps1, ps2, rs, pf1, pf2, rf, PROD_MOD, COEF_MOD):
    """
    【函数功能】计算线段集的电位系数/电感矩阵
    【入参】
    ps1(numpy.ndarray: n*3): n条线的起始点坐标矩阵
    ps2(numpy.ndarray: n*3): n条线的终止点坐标矩阵
    rs(numpy.ndarray: n*1): n条线的半径矩阵
    PROD_MOD(int): 计算模式(1 for dot product, 2 for vector product)
    COEF_MOD(int): 计算内容(1 for 电位系数potential (P), 2 for 电感inductance (L))

    【出参】
    INT(numpy.ndarray: n*n): 电位系数矩阵((COEF_MOD == 1))/n条线段的电感矩阵(COEF_MOD == 2)
    """
    # (0) initialization
    g0 = 1e-5
    d0 = 1e-6
    r0 = 1e-10

    # get the size of matrix
    Ns = len(ps1[:, 0])  # report error if len directly
    Nf = len(pf1[:, 0])
    # 定义rs和rf
    rs = rs.reshape(Ns, 1)
    rf = rf.reshape(Nf, 1)
    # a = ps1 - ps2
    ls2 = np.sum((ps1 - ps2) * (ps1 - ps2), axis=1)
    lf2 = np.sum((pf1 - pf2) * (pf1 - pf2), axis=1)
    # ls2 = [round(num, 2) for num in ls2]
    # lf2 = [round(num, 2) for num in lf2]
    # 无法使用np.round四舍五入，强制保留小数，其中  只能现在这么操作了 ，其中的2代表保留几位小数（已解决）
    ls2_elements = ls2.size
    lf2_elements = lf2.size
    if ls2_elements == 0:
        pass
    else:
        ls2_row = int(ls2_elements / Ns)
        ls2 = ls2.reshape(Ns, ls2_row)
    if lf2_elements == 0:
        pass
    else:
        lf2_row = int(lf2_elements / Nf)
        lf2 = lf2.reshape(Nf, lf2_row)

    ls2 = np.array(ls2, dtype=float)
    lf2 = np.array(lf2, dtype=float)
    ls = np.sqrt(ls2)
    lf = np.sqrt(lf2)

    # (1) determine the distance of 4 points
    if PROD_MOD == 1:  # dot product
        # case 1
        OMG = np.zeros((Nf, 1))
        tp = np.zeros((Nf, 1))

        # 计算两点之间距离的平方的矩阵集合
        R12 = calculate_distances(ps2, pf2)
        R22 = calculate_distances(ps2, pf1)
        R32 = calculate_distances(ps1, pf1)
        R42 = calculate_distances(ps1, pf2)
    elif PROD_MOD == 2:  # vector product
        # case 2
        OMG = np.zeros((Nf, Ns))
        tp = np.zeros((Nf, Ns))

        # ensure matrix has elements in all positions
        ls = np.matlib.repmat(np.transpose(ls), Nf, 1)
        lf = np.matlib.repmat(lf, 1, Ns)
        ls2 = np.matlib.repmat(np.transpose(ls2), Nf, 1)
        lf2 = np.matlib.repmat(lf2, 1, Ns)

        # 如果你需要保持二维形状，即形状为 (m, 1) 而不是 (m,)，你需要显式地进行重塑操作：
        # column_2d = my_array[:, j:j+1]  # 保持二维形状
        a = np.tile(pf2[:, 0: 1], (1, Ns))
        b = np.tile(np.transpose(ps2[:, 0: 1]), (Nf, 1))
        dx = np.tile(pf2[:, 0: 1], (1, Ns)) - np.tile(np.transpose(ps2[:, 0: 1]), (Nf, 1))  # transpose matrix
        dy = np.tile(pf2[:, 1: 2], (1, Ns)) - np.tile(np.transpose(ps2[:, 1: 2]), (Nf, 1))
        dz = np.tile(pf2[:, 2: 3], (1, Ns)) - np.tile(np.transpose(ps2[:, 2: 3]), (Nf, 1))
        R12 = dx ** 2 + dy ** 2 + dz ** 2

        dx = np.tile(pf1[:, 0: 1], (1, Ns)) - np.tile(np.transpose(ps2[:, 0: 1]), (Nf, 1))
        dy = np.tile(pf1[:, 1: 2], (1, Ns)) - np.tile(np.transpose(ps2[:, 1: 2]), (Nf, 1))
        dz = np.tile(pf1[:, 2: 3], (1, Ns)) - np.tile(np.transpose(ps2[:, 2: 3]), (Nf, 1))
        R22 = dx ** 2 + dy ** 2 + dz ** 2

        dx = np.tile(pf1[:, 0: 1], (1, Ns)) - np.tile(np.transpose(ps1[:, 0: 1]), (Nf, 1))
        dy = np.tile(pf1[:, 1: 2], (1, Ns)) - np.tile(np.transpose(ps1[:, 1: 2]), (Nf, 1))
        dz = np.tile(pf1[:, 2: 3], (1, Ns)) - np.tile(np.transpose(ps1[:, 2: 3]), (Nf, 1))
        R32 = dx ** 2 + dy ** 2 + dz ** 2

        dx = np.tile(pf2[:, 0: 1], (1, Ns)) - np.tile(np.transpose(ps1[:, 0: 1]), (Nf, 1))
        dy = np.tile(pf2[:, 1: 2], (1, Ns)) - np.tile(np.transpose(ps1[:, 1: 2]), (Nf, 1))
        dz = np.tile(pf2[:, 2: 3], (1, Ns)) - np.tile(np.transpose(ps1[:, 2: 3]), (Nf, 1))
        R42 = dx ** 2 + dy ** 2 + dz ** 2

    else:
        print('No such case in INT_ARBI_2D')
        exit()

    R12 = np.array(R12, dtype=float)
    R22 = np.array(R22, dtype=float)
    R32 = np.array(R32, dtype=float)
    R42 = np.array(R42, dtype=float)
    # get the distance between each point
    R1 = np.sqrt(R12)  # pf2-ps2
    R2 = np.sqrt(R22)  # pf1-ps2
    R3 = np.sqrt(R32)  # pf1-ps1
    R4 = np.sqrt(R42)  # pf2-ps1

    # (2) find the cos and sin
    a2 = (R42 - R32 + R22 - R12)
    cose = a2 / (2 * ls * lf)
    sine2 = 1 - cose ** 2

    # 存在负数的情况
    sine = np.sqrt(sine2.astype(complex))
    # (2a) update u (alpha) and v (beta)
    DIS = 4 * ls2 * lf2 - a2 * a2

    par1 = cose > 1 - g0  # parallel lines 1
    par2 = cose < g0 - 1  # parallel lines 2

    # 存在负号的形式
    para = np.logical_or(par1, par2)
    sign = np.where(par1, 1, 0) - np.where(par2, 1, 0)
    sign = sign[para]  # sign for lf

    u = np.array(ls * ((2 * lf2 * (R22 - R32 - ls2) + a2 * (R42 - R32 - lf2)) / DIS))
    v = (lf * ((2 * ls2 * (R42 - R32 - lf2) + a2 * (R22 - R32 - ls2)) / DIS))
    u[para] = 0
    v[para] = -(R22[para] - R32[para] - ls2[para]) / (2 * ls[para])  # parallel lines

    d2 = abs(R32 - u ** 2 - v ** 2 + 2 * u * v * cose)
    d = (np.sqrt(d2))

    copn = d < d0  # co-plane
    Itmp = para | copn  # both co-plane and parallel lines
    id = ~Itmp  # lines other than Itmp


    R1 = np.maximum(r0, R1)  # avoid zero distance
    R2 = np.maximum(r0, R2)
    R3 = np.maximum(r0, R3)
    R4 = np.maximum(r0, R4)

    # (3) lines in different planes and non-parallel lines
    OMG[id] = (np.arctan(np.real((d2[id] * cose[id] + (u[id] + ls[id]) * (v[id] + lf[id]) * sine2[id]) / (d[id] * R1[id] * sine[id])))
                - np.arctan(np.real((d2[id] * cose[id] + (u[id] + ls[id]) * v[id] * sine2[id]) / (d[id] * R2[id] * sine[id])))
                + np.arctan(np.real((d2[id] * cose[id] + (u[id] * v[id]) * sine2[id]) / (d[id] * R3[id] * sine[id])))
                - np.arctan(np.real((d2[id] * cose[id] + u[id] * (v[id] + lf[id]) * sine2[id]) / (d[id] * R4[id] * sine[id]))))

    # (4) main item (end pt positioned on the another line)
    INT = 0
    tp0 = lf / (R1 + R2)
    tp1 = (u + ls) * np.arctanh(tp0)
    tp1[abs(tp0 - 1) < r0] = 0
    INT = INT + tp1

    tp0 = ls / (R1 + R4)
    tp1 = (v + lf) * np.arctanh(tp0)
    tp1[abs(tp0 - 1) < r0] = 0
    INT = INT + tp1

    tp0 = lf / (R3 + R4)
    tp1 = u * np.arctanh(tp0)
    tp1[abs(tp0 - 1) < r0] = 0
    INT = INT - tp1

    tp0 = ls / (R2 + R3)
    tp1 = v * np.arctanh(tp0)
    tp1[abs(tp0 - 1) < r0] = 0
    INT = INT - tp1

    tp0 = OMG * d / sine
    tp0[abs(sine) < g0] = 0
    INT = 2 * INT - tp0
    INT = np.real(INT)  # 输出将只包含实数部分


    # (5) update integral with parallel line results

    if len(rf) == 1:  # rf是个数 取不了长度到时候可以再改改
        Rf = np.tile(rf, (Nf, Ns))
    else:
        Rf = np.tile(rf, (1, Ns))
    if len(rs) == 1:  #
        Rs = np.tile(rs, (Nf, Ns))
    else:
        Rs = np.tile(np.transpose(rs), (Nf, 1))  #

    rows, cols = np.where(para)

    out = INT_LINE_D2P_D(tp[rows, cols], ls[rows, cols], tp[rows, cols], 0, \
                                Rs[rows, cols], v[rows, cols], v[rows, cols] + sign * lf[rows, cols], d[rows, cols], 0, Rf[rows, cols])
    INT[rows, cols] = np.abs(out)

    # (6) check whether it is the integral for inductance or potential
    if COEF_MOD == 2:  # inductance
        INT = cose * INT

    # return result
    return INT



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


def calculate_potential(ps1, ps2, ls, rs, pf1, pf2, lf, rf, At, Nnode):

    # (2) Generating coordinates of node segments (half of bran segments)
    ps0 = 0.5 * (ps1 + ps2)
    pf0 = 0.5 * (pf1 + pf2)
    ofs = 0

    # init
    ps1_len = len(ps1)
    rs = rs.reshape(ps1_len, 1)
    rf = rf.reshape(ps1_len, 1)
    ls = ls.reshape(ps1_len, 1)
    lf = lf.reshape(ps1_len, 1)
    N = ps1_len * 2
    nrs = np.zeros((N, 1))
    nls = np.zeros((N, 1))
    nps1 = np.zeros((N, 3))
    nps2 = np.zeros((N, 3))
    nrf = np.zeros((N, 1))
    nlf = np.zeros((N, 1))
    npf1 = np.zeros((N, 3))
    npf2 = np.zeros((N, 3))
    ncom = np.zeros((Nnode, 1))

    for ik in range(int(np.min(At)), int(np.min(At))+Nnode):  # size of node segments for source
        pt1 = np.where(At[:, 0] == ik)[0]  # pos of ith node in branch
        pt2 = np.where(At[:, 1] == ik)[0]  # pos of ith node in branch
        d1 = len(pt1)  # total # of common nodes for ith node
        d2 = len(pt2)  # total # of common nodes for ith node

        # (2a) 1st half segment
        if d1 != 0:
            indices = slice(ofs, ofs + d1)
            nrs[indices, 0:1] = rs[pt1]  # radius (n1)-source
            nls[indices, 0:1] = ls[pt1] / 2  # length (n1)
            nps1[indices, 0:3] = ps1[pt1, 0:3]  # start points
            nps2[indices, 0:3] = ps0[pt1, 0:3]  # end points

            nrf[indices, 0:1] = rf[pt1]  # radius(n1)-field
            nlf[indices, 0:1] = lf[pt1] / 2  # length(n1)
            npf1[indices, 0:3] = pf1[pt1, 0:3]  # start points
            npf2[indices, 0:3] = pf0[pt1, 0:3]  # end points

        ofs += d1
        # (2b) 2nd half segment
        if d2 != 0:
            indices = slice(ofs, ofs + d2)
            nrs[indices, 0:1] = rs[pt2]  # radius (n2)
            nls[indices, 0:1] = ls[pt2] / 2  # length (n2)
            nps1[indices, 0:3] = ps0[pt2, 0:3]  # start points
            nps2[indices, 0:3] = ps2[pt2, 0:3]  # end points

            nrf[indices, 0:1] = rf[pt2]  # radius(n1)
            nlf[indices, 0:1] = lf[pt2] / 2  # length(n2)
            npf1[indices, 0:3] = pf0[pt2, 0:3]  # start points
            npf2[indices, 0:3] = pf2[pt2, 0:3]  # end points

        ofs += d2
        ncom[ik - int(np.min(At)) - 1] = d1 + d2  # of segments for each node

    # (4) Calculating potential matrix
    PROD_MOD = 2  # matrix product
    COEF_MOD = 1  # integration only

    INT = INT_SLAN_2D(nps1, nps2, nrs, npf1, npf2, nrf, PROD_MOD, COEF_MOD)

    # (5) merging common nodes
    P = INT

    Idel = []  # 假设 Idel 是一个已经初始化的列表
    ofs = 0  # 假设 ofs 是一个初始偏移量
    nlns = np.zeros((Nnode, 1))  # 初始化 nlns
    nlnf = np.zeros((Nnode, 1))  # 初始化 nlnf

    for ik in range(Nnode):
        nc = ncom[ik][0]  # of common nodes for ith node
        nc = int(nc)
        if nc >= 1:
            Idel.extend(range(ofs + 1, ofs + nc))  # collecting deleted row/col
        # 使用切片来求和
        nlns[ik] = np.sum(nls[ofs:ofs + nc])  # total length of ith node (source)
        nlnf[ik] = np.sum(nlf[ofs:ofs + nc])  # total length of ith node (field)

        # 收集共同节点的行和列
        tmp = P[ofs:ofs + nc, :]  # collecting rows of common nodes
        P[ofs, :] = np.sum(tmp, axis=0)  # sum of all rows
        tmp = P[:, ofs:ofs + nc]  # collecting cols of common nodes
        P[:, ofs] = np.sum(tmp, axis=1)  # sum of all cols

        ofs += nc

    P = np.delete(P, Idel, axis=0)
    P = np.delete(P, Idel, axis=1)
    P = P / (nlns * np.transpose(nlnf))

    return P


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


def calculate_wires_inductance_potential_with_ground(wires: Wires, ground, constants):
    # （0) Intial constants
    ep0, mu0, ke, km = constants.ep0, constants.mu0, constants.ke, constants.km

    # Nba所有空气中支路的数量
    Nba = wires.count_airWires()
    # Ngn所有地面支路的数量
    Ngn = wires.count_gndWires()
    # Nna所有空气中节点的数量
    Nna = wires.count_distinct_airPoints()
    # Nng所有地面节点的数量
    Nng = wires.count_distinct_gndPoints()

    # Nn所有节点的数量, 默认空气中节点和地面节点无重复, 可以直接相加 
    Nn = Nna + Nng
    # rb1 空气中的支路index集合(n*1)
    # 由于支路和节点矩阵，都是根据air_wires -> ground_wires -> a2g_wires -> short_wires -> tube_wires顺序进行拼接，因此可以通过支路数量进行数据切分，取出空气中和地面的线段的参数
    rb1 = np.arange(0, Nba)  # air bran
    rb1 = rb1.flatten()
    # rb2 地面导线的支路index集合（n*1）
    rb2 = np.arange(Nba, Nba + Ngn)  # gnd bran
    rb2 = rb2.flatten()
    # rn1 空气中节点index（n*1）
    rn1 = np.arange(0, Nna)  # air node
    rn1 = rn1.flatten()
    # rn2 地面导线的节点index（n*1）
    rn2 = np.arange(Nna, Nna + Nng)  # gnd node,此处可能会有问题，因为wires不仅只包含空气中导线和地面导线，数据切分可能会有问题，应该为np.arange(空气导线数量, 空气导线数量+地面导线数量)
    rn2 = rn2.flatten()

    # (1) Obtain L and P matrices without considering the ground effect

    start_points = wires.get_start_points()
    end_points = wires.get_end_points()
    radii = wires.get_radii()
    lengths = wires.get_lengths()
    At = wires.get_bran_index()

    # get x_consines, y_consines and z_consines
    x_consines, y_consines, z_consines = calculate_direction_cosines(start_points, end_points, lengths)


    # WireL = ls      # output wire length (updated in 04/24)
    # for gnd and air segments
    Lout = calculate_inductance(start_points, end_points, radii, start_points, end_points, radii)
    Pout = calculate_potential(start_points, end_points, lengths, radii, start_points, end_points, lengths, radii, At, Nn)

    # (2) Constructing L and P by considering the image effect
    # no ground (0), perfect ground (1), lossy ground model (2)
    # (2a) without ground
    # free-space inductance
    L0 = Lout * (x_consines * np.transpose(x_consines) + y_consines * np.transpose(y_consines) + z_consines * np.transpose(z_consines))
    # free-space potential
    P0 = Pout

    # (2b) with ground
    # L and P matrices for aai,ggi

    if ground.gnd_model != "No":
        pf1 = start_points.copy()
        pf1[:, 2] = -pf1[:, 2]  # image for air segments
        pf2 = end_points.copy()
        pf2[:, 2] = -pf2[:, 2]  # image for gnd segments

        # 计算tmp  
        tmp = 0.5 * np.abs(pf1[:, 2] + pf2[:, 2])  # 注意MATLAB的索引从1开始，Python从0开始，所以这里是[:, 2]  
        
        # 遍历tmp和rs的索引  
        for ik in range(len(tmp)):  
            if tmp[ik] < radii[ik]:  
                pf1[ik, 2] = -2.2 * radii[ik]  # 设置间隔为2*rs  
                pf2[ik, 2] = -2.2 * radii[ik]  # 设置间隔为2*rs  

        # L and P matrices for air and gnd segments
        Lai = calculate_inductance(start_points[rb1, :], end_points[rb1, :], radii[rb1, 0], pf1[rb1, :], pf2[rb1, :], radii[rb1, 0])
        Pai = calculate_potential(start_points[rb1, :], end_points[rb1, :], lengths[rb1, 0], radii[rb1, 0], pf1[rb1, :], pf2[rb1, :], lengths[rb1, 0], radii[rb1, 0], At[rb1, :], Nna)

        Lgi = calculate_inductance(start_points[rb2, :], end_points[rb2, :], radii[rb2, 0], pf1[rb2, :], pf2[rb2, :], radii[rb2, 0])
        Pgi = calculate_potential(start_points[rb2, :], end_points[rb2, :], lengths[rb2, 0], radii[rb2, 0], pf1[rb2, :], pf2[rb2, :], lengths[rb2, 0], radii[rb2, 0], At[rb2, :], Nng)

    # (2bi) perfect ground
    if ground.gnd_model == "Perfect":
        L0 = L0 - Lai * (x_consines * np.transpose(x_consines) + y_consines * np.transpose(y_consines) + z_consines * np.transpose(z_consines))
        P0 = P0 - Pai

    # (2bii) lossy ground model
    if ground.gnd_model == "Lossy":
        if not rb1.size or not rb2.size:
            Lag = np.array([])
            Lga = np.array([])
            Pag = np.array([])
            Pga = np.array([])
        else:
            Lag = Lout[rb1[:, np.newaxis], rb2]
            Lga = Lout[rb2[:, np.newaxis], rb1]
            Pag = Pout[rn1[:, np.newaxis], rn2]
            Pga = Pout[rn2[:, np.newaxis], rn1]

        # image effect
        # (i) f./s. wire in air
        z_consinesA = z_consines[rb1]
        L0[rb1[:, np.newaxis], rb1] = L0[rb1[:, np.newaxis], rb1] + Lai * z_consinesA * np.transpose(
            z_consinesA)  # vertical contribution
        P0[rn1[:, np.newaxis], rn1] = P0[rn1[:, np.newaxis], rn1] - Pai

        if Nng != 0:
            # x_consinesG = x_consines[rb2]  # gnd wire: direction numbers
            # y_consinesG = y_consines[rb2]
            z_consinesG = z_consines[rb2]

            # (ii) f. wire in gnd s. wire in air
            L0[rb2[:, np.newaxis], rb1] = L0[rb2[:, np.newaxis], rb1] + Lga * z_consinesG * np.transpose(
                z_consinesA)  # vertical contribution
            P0[rn2[:, np.newaxis], rn1] = P0[rn2[:, np.newaxis], rn1] - Pga

            # (iii) f./s. wire in gnd
            L0[rb2[:, np.newaxis], rb2] = L0[rb2[:, np.newaxis], rb2] - Lgi * z_consinesG * np.transpose(
                z_consinesG)  # vertical contribution
            P0[rn2[:, np.newaxis], rn2] = P0[rn2[:, np.newaxis], rn2] + Pgi

            # (iv) f. wire in air s. wire in gnd
            L0[rb1[:, np.newaxis], rb2] = L0[rb1[:, np.newaxis], rb2] - Lag * z_consinesA * np.transpose(
                z_consinesG)  # vertical contribution
            P0[rn1[:, np.newaxis], rn2] = P0[rn1[:, np.newaxis], rn2] + Pag

    L0 = km * L0
    P0 = ke * P0
    return L0, P0