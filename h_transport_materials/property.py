import numpy as np
from h_transport_materials import k_B

class Property:
    def __init__(self, source: str="", name : str="", range: tuple=None, data_T: list=None, data_y: list=None) -> None:
        self.source = source
        self.name = name
        self.range = range
        self.data_T = data_T
        self.data_y = data_y
    
    def value(self, T):
        pass


class ArheniusProperty(Property):
    def __init__(self, pre_exp: float, act_energy: float, **kwargs) -> None:
        self.pre_exp = pre_exp
        self.act_energy = act_energy
        super().__init__(**kwargs)

    def value(self, T, exp=np.exp):
        return self.pre_exp * exp(-self.act_energy/k_B/T)
