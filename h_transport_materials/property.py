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
        """Inits Property

        Args:
            material (str, optional): name of the material. Defaults to "".
            source (str, optional): bibliographic reference. Defaults to "".
            name (str, optional): name of the property. Defaults to "".
            range (tuple, optional): temperature validity range in K.
                Defaults to None.
            year (int, optional): year of publication. Defaults to None.
            isotope (str, optional): isotope of the property ("H", "D" or "T").
                Defaults to None.
            author (str, optional): name of the author. Defaults to "".
        """

        self.material = material
        self.source = source
        self.name = name
        self.range = range
        self.year = year
        self.isotope = isotope
        self.author = author

    def value(self, T):
        pass


class ArrheniusProperty(Property):
    def __init__(
        self,
        pre_exp: float = None,
        act_energy: float = None,
        data_T: list = None,
        data_y: list = None,
        **kwargs
    ) -> None:
        """Inits ArrheniusProperty
        property = pre_exp * exp( - act_energy/(k_B T) )

        Args:
            pre_exp (float, optional): the pre-exponential factor. Defaults to None.
            act_energy (float, optional): the activation energy in eV. Defaults to None.
            data_T (list, optional): list of temperatures in K. Used to automatically
                fit experimental points. Defaults to None.
            data_y (list, optional): list of y data. Used to automatically
                fit experimental points. Defaults to None.
            kwargs: other Property arguments
        """
        self.pre_exp = pre_exp
        self.act_energy = act_energy
        self.data_T = data_T
        self.data_y = data_y
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

    @property
    def data_T(self):
        return self._data_T

    @data_T.setter
    def data_T(self, value):
        if value is None:
            self._data_T = value
            return
        if not isinstance(value, (list, np.ndarray)):
            raise TypeError("data_T accepts list or np.ndarray")
        elif isinstance(value, list):
            self._data_T = np.array(value)
        else:
            self._data_T = value

    @property
    def data_y(self):
        return self._data_y

    @data_y.setter
    def data_y(self, value):
        if value is None:
            self._data_y = value
            return
        if not isinstance(value, (list, np.ndarray)):
            raise TypeError("data_y accepts list or np.ndarray")
        elif isinstance(value, list):
            self._data_y = np.array(value)
        else:
            self._data_y = value

    def fit(self):
        self.pre_exp, self.act_energy = fit_arhenius(self.data_y, self.data_T)

    def value(self, T, exp=np.exp):
        return self.pre_exp * exp(-self.act_energy / k_B / T)
