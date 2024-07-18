import math

class StrokeParameters:
    CIGRE_PARAMETERS = {
        '0.25/100us': [0.25, 100, 6.4, 2, 0.9, 30, 0.5, 80, 2, 0.7],
        '8/20us': [8, 20, 1.18, 2.6, 0.93, 19.9, 0.51, 50, 1.5, 0.4],
        '2.6/50us': [2.6, 50, 2.56, 2.1, 0.92, 30, 0.5, 80, 1.8, 0.6],
        '10/350us': [10, 350, 0.92, 2.1, 0.98, 45, 0.53, 160, 2, 0.7]
    }

    HEIDLER_PARAMETERS = {
        '0.25/100us': [0.9, 0.25, 100, 2],
        '8/20us': [30.85, 8, 20, 2.4],
        '2.6/50us': [16.83, 2.6, 50, 2.1],
        '10/350us': [44.43, 10, 350, 2.1]
    }


class Stroke:
    def __init__(self, stroke_type: str, duration:float, is_calculated: bool, parameter_set: str, parameters=None):
        """
        初始化脉冲对象
        
        参数说明:
        stroke_type (str): 脉冲的类型, 目前只支持 'CIGRE' 和 'Heidler'
        duration (float): 脉冲持续时间
        is_calculated (bool): 脉冲是否要被计算
        parameter_set (str): 脉冲参数集, 目前只支持 '0.25/100us', '8/20us', '2.6/50us', '10/350us'
        parameters (list, optional): 脉冲参数, 仅在 'CIGRE' 和 'Heidler' 类型时使用, parameter_set被指定时, 请勿初始化该参数, 如想测试parameter_set之外的参数集, 请在此处初始化参数列表
        """
        self.stroke_type = stroke_type
        self.duration = duration
        self.is_calculated = is_calculated
        # parameter_set与parameters二选一传入，最终决定参数列表归属
        if parameter_set:
            if stroke_type == 'CIGRE':
                self.parameters = StrokeParameters.CIGRE_PARAMETERS[parameter_set]
            elif stroke_type == 'Heidler':
                self.parameters = StrokeParameters.HEIDLER_PARAMETERS[parameter_set]
            else:
                raise ValueError("Invalid stroke type. Must be 'CIGRE' or 'Heidler'.")

        if parameters:
            self.parameters = parameters

    def cigre_waveform(self, t):
        tn, A, B, n, I1, t1, I2, t2, Ipi, Ipc = self.parameters
        return I1 * (math.exp(-t/t1) - math.exp(-t/t2)) + Ipi * (1 - math.exp(-t/tn))**n + Ipc

    def heidler_waveform(self, t):
        Ip, Tf, tau, n = self.parameters
        return Ip * (t/Tf) * ((t/Tf)**(n-1)) * math.exp(-(t/Tf)**n) / ((1 + (t/tau)**2)**(n/2))

    def calculate(self, t):
        """
        Calculate the pulse waveform at the given time.
        
        Args:
            t (float): Time in seconds.
        
        Returns:
            float: The value of the pulse waveform at the given time.
        """
        # Calculate only when is_calculated==True
        if self.is_calculated:
            if self.stroke_type == 'CIGRE':
                return self.cigre_waveform(t)
            elif self.stroke_type == 'Heidler':
                return self.heidler_waveform(t)
        return 0


class Lightning:
    def __init__(self, id:int, type:str, strokes):
        """
        初始化雷电对象

        参数说明:
        id (int): 雷电序号
        type (str): 雷电类型, 请指定'Direct'或'Indirect', 用以表示直击雷或间接雷
        strokes (list, optional): 雷电的脉冲列表, 如未指定, 默认为空列表
        """
        self.id = id
        self.type = type
        self.strokes = strokes or []
        self.stroke_number = len(self.strokes)


    def add_stroke(self, stroke: Stroke):
        self.strokes.append(stroke)
        self.stroke_number = len(self.strokes)


    def total_waveform(self, t):
        """
        Calculate the total lightning waveform at the given time.
        
        Args:
            t (float): Time in seconds.
        
        Returns:
            float: The value of the total lightning waveform at the given time.
        """
        total = 0
        for stroke in self.strokes:
            total += stroke.calculate(t)
        return total