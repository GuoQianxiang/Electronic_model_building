import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from Wires import LumpWire

class Component:
    def __init__(self, name: str, parameters: dict = None):
        """
        基础元件的抽象基类。

        Args:
            name (str): 元件名称。
            parameters (dict, optional): 元件参数的字典。默认为空字典。
        """
        self.name = name
        self.parameters = parameters if parameters is not None else {}

    def calculate(self, *args, **kwargs):
        """
        计算元件的电路响应。需要在具体的子类中实现。

        Raises:
            NotImplementedError: 如果在子类中未实现该方法。
        """
        raise NotImplementedError("calculate method must be implemented in subclasses")


class Resistor(Component):
    def __init__(self, name: str, resistance: float):
        """
        电阻器类，继承自 Component 类。

        Args:
            name (str): 电阻器名称。
            resistance (float): 电阻值。
        """
        super().__init__(name, {"resistance": resistance})

    def calculate(self, *args, **kwargs):
        # 实现电阻器的电路响应计算逻辑
        pass


class Capacitor(Component):
    def __init__(self, name: str, capacitance: float):
        """
        电容器类，继承自 Component 类。

        Args:
            name (str): 电容器名称。
            capacitance (float): 电容值。
        """
        super().__init__(name, {"capacitance": capacitance})

    def calculate(self, *args, **kwargs):
        # 实现电容器的电路响应计算逻辑
        pass


class Circuit:
    def __init__(self):
        """
        电路图类表示整个电路。
        wires(list): 导线线段集合
        components(list): 集中参数元件集合
        """
        self.wires = []
        self.components = []

    def add_wire(self, wire: LumpWire):
        """
        向电路中添加一条新的导线。

        Args:
            wire (Wire): 要添加的导线对象。
        """
        self.wires.append(wire)

    def add_component(self, component: Component):
        """
        向电路中添加一个新的基础元件。

        Args:
            component (Component): 要添加的基础元件对象。
        """
        self.components.append(component)

    def connect_component_to_wire(self, component: Component, wire: LumpWire):
        """
        将一个基础元件连接到指定的导线上。

        Args:
            component (Component): 要连接的基础元件对象。
            wire (Wire): 要连接到的导线对象。
        """
        wire.add_component(component)