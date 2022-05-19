from h_transport_materials import Property, ArrheniusProperty

try:
    import FESTIM
except ModuleNotFoundError:
    pass
    # print("FESTIM module not found")


class Material:
    def __init__(
        self,
        D: ArrheniusProperty,
        S: ArrheniusProperty,
        lambd=None,
        rho=None,
        cp=None,
        name: str = None,
    ):
        self.D = D
        self.S = S
        self.lambd = lambd
        self.rho = rho
        self.cp = cp
        self.name = name

        self.festim_material = None

    def make_festim_material(self):
        return FESTIM.Material(
            D_0=self.D.pre_exp,
            E_D=self.D.act_energy,
            S_0=self.S.pre_exp,
            E_S=self.S.act_energy,
        )
