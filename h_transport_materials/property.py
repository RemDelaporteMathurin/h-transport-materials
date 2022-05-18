import numpy as np
from h_transport_materials import k_B
from h_transport_materials.fitting import fit_arhenius


class Property:
    def __init__(
        self,
        material: str = "",
        source: str = "",
        name: str = "",
        range: tuple = None,
        year: int = None,
        isotope: str = None,
        author: str = "",
    ) -> None:

        self.material = material
        self.source = source
        self.name = name
        self.range = range
        self.year = year
        self.isotope = isotope
        self.author = author

    def value(self, T):
        pass


class ArheniusProperty(Property):
    def __init__(
        self,
        pre_exp: float = None,
        act_energy: float = None,
        data_T: list = None,
        data_y: list = None,
        act_energy_units: str = "eV",
        **kwargs
    ) -> None:
        self.pre_exp = pre_exp
        self.act_energy = act_energy
        self.data_T = data_T
        self.data_y = data_y
        self.act_energy_units = act_energy_units
        super().__init__(**kwargs)

    @property
    def pre_exp(self):
        if self._pre_exp is None and self.data_T is not None:
            self.fit()
        return self._pre_exp

    @pre_exp.setter
    def pre_exp(self, value):
        self._pre_exp = value

    @property
    def act_energy(self):
        if self._act_energy is None and self.data_T is not None:
            self.fit()
        return self._act_energy

    @act_energy.setter
    def act_energy(self, value):
        self._act_energy = value

    def fit(self):
        self.pre_exp, self.act_energy = fit_arhenius(self.data_y, self.data_T)

    def value(self, T, exp=np.exp):
        return self.pre_exp * exp(-self.act_energy / k_B / T)
