import math


class Constant:
    def __init__(self):
        """
        初始化常数列表
        
        参数说明:
        ep0 (float): xxx电常数
        mu0 (float): xxx
        ke (float): xxx
        km (float): xxx
        Vair (float): xxx
        g0 (float): xxx
        d0 (float): xxx
        ELIM (float): xxx
        """
        self.ep0 = 8.854187818e-12
        self.mu0 = 4 * math.pi * 1e-7
        self.ke = 1 / (4 * math.pi * self.ep0)
        self.km = self.mu0 / (4 * math.pi)  # coef for inductance
        self.Vair = 3e8  # Velocity in free space
        self.g0 = 1e-5
        self.d0 = 1e-6
        self.r0 = 1e-10
        self.ELIM = 1e-9  # limit for changing formula