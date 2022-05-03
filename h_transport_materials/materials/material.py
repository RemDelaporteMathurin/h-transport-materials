from h_transport_materials import Property

class Material:
    def __init__(self, D, S, lambd=None, rho=None, cp=None, name: str=None):
        self.D = D
        self.S = S
        self.lambd = lambd
        self.rho = rho
        self.cp = cp
        self.name = name