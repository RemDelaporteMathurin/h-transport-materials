from collections.abc import Iterable
import numpy as np
from crossref.restful import Works, Etiquette
import pint
from pybtex.database import BibliographyData, parse_string
from h_transport_materials import k_B, bib_database, ureg
from h_transport_materials.fitting import fit_arhenius

import warnings

DEFAULT_ENERGY_UNITS = ureg.eV * ureg.particle**-1


class Property:
    """Base Property class

    Args:
        material (str, optional): name of the material. Defaults to "".
        source (str, optional): bibliographic reference. Defaults to "".
        range (tuple, optional): temperature validity range in K.
            Defaults to None.
        year (int, optional): year of publication. Defaults to None.
        isotope (str, optional): isotope of the property ("H", "D" or "T").
            Defaults to None.
        author (str, optional): name of the author. Defaults to "".
        note (str, optional): additional information. Defaults to None.
    """

    def __init__(
        self,
        material: str = "",
        source: str = "",
        range: tuple = None,
        year: int = None,
        isotope: str = None,
        author: str = "",
        note: str = None,
    ) -> None:
        self.material = material
        self.source = source
        self.range = range
        self.isotope = isotope
        self.note = note

        self.nb_citations = None

        # make bibsource
        if source in bib_database.entries:
            self.bibsource = bib_database.entries[source]
        elif self.source.startswith("@"):
            self.bibsource = list(
                parse_string(self.source, bib_format="bibtex").entries.values()
            )[0]
        else:
            self.bibsource = None

        # try get year and author from bibsource
        if self.bibsource:
            self.year = int(self.bibsource.fields["year"])
            if year is not None:
                warnings.warn(
                    "year argument will be ignored since a bib source was found"
                )
            self.author = self.bibsource.persons["author"][0].last_names[0].lower()
            if author != "":
                warnings.warn(
                    "author argument will be ignored since a bib source was found"
                )
        else:
            self.author = author
            self.year = year

    @property
    def bibdata(self):
        if self.bibsource is None:
            raise ValueError("No bibsource found")

        bibdata = {self.bibsource.key: self.bibsource}
        return BibliographyData(bibdata)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        if value:
            if not isinstance(value, Iterable):
                raise TypeError("range should be an iterable containing two values")
            if len(value) != 2:
                raise TypeError("range should be an iterable containing two values")

            if value[0] <= 0 or value[1] <= 0:
                raise ValueError("temperature range must be stricly positive (Kelvin)")

        self._range = value

    @property
    def doi(self):
        self._doi = None
        if self.bibsource:
            if "doi" in self.bibsource.fields:
                self._doi = self.bibsource.fields["doi"]

        return self._doi

    @doi.setter
    def doi(self, value):
        self._doi = value

    @property
    def nb_citations(self):
        # if nb_citations doesn't already exist, compute it
        if self._nb_citations is None:
            if self.bibsource is None:
                self.nb_citations = 0
            elif self.doi:
                self.nb_citations = get_nb_citations(self.doi)
            else:
                self.nb_citations = 0
        return self._nb_citations

    @nb_citations.setter
    def nb_citations(self, value):
        self._nb_citations = value

    def export_bib(self, filename: str):
        """Exports the property reference to bib

        Args:
            filename (str): the filename

        Raises:
            ValueError: if the property bibsource attribute is None
        """

        self.bibdata.to_file(filename)

    def to_json(self):
        """Returns a dictionary with the relevant attributes of the property

        Returns:
            dict: a dict reprensation of the property
        """
        as_json = {}
        if self.range is not None:
            as_json["range"] = {}
            as_json["range"]["value"] = (
                self.range[0].magnitude,
                self.range[1].magnitude,
            )
            as_json["range"]["units"] = f"{self.range[0].units}"
        as_json["material"] = self.material.name
        as_json["source"] = self.source
        as_json["year"] = self.year
        as_json["isotope"] = self.isotope
        as_json["author"] = self.author
        as_json["note"] = self.note
        as_json["doi"] = self.doi
        as_json["type"] = self.__class__.__name__

        return as_json

    def value(self, T):
        pass


class ArrheniusProperty(Property):
    """
    Arrhenius type Property
    value = pre_exp * exp( - act_energy/(k_B T) )

    Args:
        pre_exp (float or pint.Quantity, optional): the pre-exponential factor. Defaults to None.
        act_energy (float or pint.Quantity, optional): the activation energy. Defaults to None.
        data_T (list, optional): list of temperatures in K. Used to automatically
            fit experimental points. Defaults to None.
        data_y (list, optional): list of y data. Used to automatically
            fit experimental points. Defaults to None.
        kwargs: other Property arguments
    """

    def __init__(
        self,
        pre_exp: float = None,
        act_energy: float = None,
        data_T: list = None,
        data_y: list = None,
        **kwargs,
    ) -> None:
        self.pre_exp = pre_exp
        self.act_energy = act_energy
        self.data_T = data_T
        self.data_y = data_y
        super().__init__(**kwargs)

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp:.2e~P}
        Activation energy: {self.act_energy:.2e~P}
        """
        return val

    @property
    def units(self):
        # check if data_y is set
        if hasattr(self, "data_y"):
            if self.data_y is not None:
                return self.data_y.units
        # check if pre_exp is set
        if hasattr(self, "pre_exp"):
            return self.pre_exp.units

        # return dimensionless by default
        return ureg.dimensionless

    @property
    def range(self):
        if self._range is None and self.data_T is not None:
            self.fit()
        return self._range

    @range.setter
    def range(self, value):
        if value is None:
            self._range = value
            return

        range_min, range_max = value
        if isinstance(range_min, pint.Quantity):
            if self.units != ureg.dimensionless:
                self._range = (range_min.to(ureg.K), range_max.to(ureg.K))
            else:
                self._range = (range_min, range_max)
        else:
            # assume it's given in the correct units
            warnings.warn(
                f"no units were given with temperature range, assuming {ureg.K:~}"
            )
            self._range = (
                pint.Quantity(value[0], ureg.K),
                pint.Quantity(value[1], ureg.K),
            )

    @property
    def pre_exp(self):
        if self._pre_exp is None and self.data_T is not None:
            self.fit()
        return self._pre_exp

    @pre_exp.setter
    def pre_exp(self, value):
        if isinstance(value, pint.Quantity):
            if self.units != ureg.dimensionless:
                self._pre_exp = value.to(self.units)
            else:
                self._pre_exp = value

        elif value is not None:
            # assume it's given in the correct units
            warnings.warn(
                f"no units were given with pre-exponential factor, assuming {self.units:~}"
            )
            self._pre_exp = value * self.units
        else:
            self._pre_exp = value

    @property
    def act_energy(self):
        if self._act_energy is None and self.data_T is not None:
            self.fit()
        return self._act_energy

    @act_energy.setter
    def act_energy(self, value):
        if isinstance(value, pint.Quantity):
            self._act_energy = value.to(DEFAULT_ENERGY_UNITS)
        elif value is not None:
            # assume it's given in DEFAULT_ENERGY_UNITS
            warnings.warn(
                f"no units were given with activation energy, assuming {DEFAULT_ENERGY_UNITS:~}"
            )
            self._act_energy = value * DEFAULT_ENERGY_UNITS
        else:
            self._act_energy = value

    @property
    def data_T(self):
        return self._data_T

    @data_T.setter
    def data_T(self, value):
        if value is None:
            self._data_T = value
            return
        if isinstance(value, pint.Quantity):
            # convert to K
            value = value.to(ureg.K)
        else:
            warnings.warn(f"no units were given with data_T, assuming {ureg.K:~}")
            value *= ureg.K

        value = self._remove_nan_in_experimental_points(value)

        self._data_T = value

    @property
    def data_y(self):
        return self._data_y

    @data_y.setter
    def data_y(self, value):
        if value is None:
            self._data_y = value
            return
        if isinstance(value, pint.Quantity):
            # convert to right units
            if self.units != ureg.dimensionless:
                value = value.to(self.units)
            else:
                value = value
        else:
            warnings.warn(f"no units were given with data_y, assuming {self.units:~}")
            value *= self.units
        value = self._remove_nan_in_experimental_points(value)

        self._data_y = value

    def _remove_nan_in_experimental_points(self, quantity: pint.Quantity):
        """Removes all nan values from a list of values

        Args:
            quantity (pint.Quantity): the quantity with magnitude as a list

        Raises:
            TypeError: if the magnitude is not a list of a numpy array

        Returns:
            pint.Quantity: the values without nans
        """
        if not isinstance(quantity.magnitude, (list, np.ndarray)):
            raise TypeError("data_T and data_y accept list or np.ndarray")
        quantity_mag = np.asarray(quantity.magnitude)
        quantity_mag = quantity_mag[~np.isnan(quantity_mag)]

        return ureg.Quantity(quantity_mag, quantity.units)

    def fit(self):
        pre_exp, act_energy = fit_arhenius(self.data_y, self.data_T)
        self.pre_exp, self.act_energy = (
            pre_exp * self.units,
            act_energy * DEFAULT_ENERGY_UNITS,
        )
        self.range = (self.data_T.min(), self.data_T.max())

    def value(self, T, exp=np.exp):
        if not isinstance(T, pint.Quantity):
            warnings.warn(f"no units were given with T, assuming {ureg.K}")
            T *= ureg.K
        return self.pre_exp * exp(-self.act_energy / k_B / T)

    def to_json(self):
        """Returns a dictionary with the relevant attributes of the property

        Returns:
            dict: a dict reprensation of the property
        """
        as_json = super().to_json()
        as_json["pre_exp"] = {}
        as_json["act_energy"] = {}
        as_json["pre_exp"]["value"] = self.pre_exp.magnitude
        as_json["pre_exp"]["units"] = f"{self.pre_exp.units}"
        as_json["act_energy"]["value"] = self.act_energy.magnitude
        as_json["act_energy"]["units"] = f"{self.act_energy.units}"
        if self.data_T is not None:
            as_json["data_T"] = {}
            as_json["data_T"]["value"] = self.data_T.magnitude.tolist()
            as_json["data_T"]["units"] = f"{self.data_T.units}"
        if self.data_y is not None:
            as_json["data_y"] = {}
            as_json["data_y"]["value"] = self.data_y.magnitude.tolist()
            as_json["data_y"]["units"] = f"{self.data_y.units}"
        return as_json


class Solubility(ArrheniusProperty):
    """Solubility class

    Args:
        S_0 (float or pint.Quantity, optional): pre-exponential factor. Defaults to None.
        E_S (float or pint.Quantity, optional): activation energy. Defaults to None.
        law (str, optional): "sievert" or "henry", the solubility law
    """

    def __init__(
        self, S_0: float = None, E_S: float = None, law: str = None, **kwargs
    ) -> None:
        self.law = law
        super().__init__(pre_exp=S_0, act_energy=E_S, **kwargs)

    @property
    def law(self):
        return self._law

    @law.setter
    def law(self, value):
        acceptable_values = ["sievert", "henry", None]
        if value not in acceptable_values:
            raise ValueError(f"law should be one of {acceptable_values}, not {value}")
        self._law = value

    @ArrheniusProperty.pre_exp.setter
    def pre_exp(self, value):
        if value is None:
            self._pre_exp = value
            return
        if isinstance(value, pint.Quantity):
            self.set_law_from_quantity(value)

            self._pre_exp = value.to(self.units)
        elif self.law is None:
            raise ValueError(
                "units are required for Solubility.pre_exp, set law argument for default units"
            )
        else:
            warnings.warn(
                f"no units were given with pre-exponential factor, assuming {self.units:~}"
            )
            self._pre_exp = value * self.units

    @ArrheniusProperty.data_y.setter
    def data_y(self, value):
        if value is None:
            self._data_y = value
            return
        if isinstance(value, pint.Quantity):
            self.set_law_from_quantity(value)

            # convert to right units
            value = value.to(self.units)
        else:
            raise ValueError("units are required for Solubility")
        value = self._remove_nan_in_experimental_points(value)

        self._data_y = value

    def set_law_from_quantity(self, quantity):
        sievert_units = ureg.particle * ureg.meter**-3 * ureg.Pa**-0.5
        henry_units = ureg.particle * ureg.meter**-3 * ureg.Pa**-1
        if quantity.check(sievert_units):
            self.law = "sievert"
        elif quantity.check(henry_units):
            self.law = "henry"
        else:
            raise ValueError(
                f"Wrong dimensionality for solubility. Should be one of {[henry_units.dimensionality, sievert_units.dimensionality]}"
            )

    @property
    def units(self):
        if self.law == "sievert":
            return ureg.particle * ureg.meter**-3 * ureg.Pa**-0.5
        elif self.law == "henry":
            return ureg.particle * ureg.meter**-3 * ureg.Pa**-1


class Diffusivity(ArrheniusProperty):
    """Diffusivity class

    Args:
        D_0 (float or pint.Quantity, optional): pre-exponential factor. Defaults to None.
        E_D (float or pint.Quantity, optional): activation energy. Defaults to None.
    """

    def __init__(self, D_0: float = None, E_D: float = None, **kwargs) -> None:
        super().__init__(pre_exp=D_0, act_energy=E_D, **kwargs)

    @property
    def units(self):
        return ureg.meter**2 * ureg.second**-1


class Permeability(ArrheniusProperty):
    """Permeability class

    Args:
        pre_exp (float or pint.Quantity, optional): the pre-exponential factor. Defaults to None.
        act_energy (float or pint.Quantity, optional): the activation energy. Defaults to None.
        data_T (list, optional): list of temperatures in K. Used to automatically
            fit experimental points. Defaults to None.
        data_y (list, optional): list of y data. Used to automatically
            fit experimental points. Defaults to None.
        law (str, optional): "sievert" or "henry", the solubility law. Defaults to None.
    """

    def __init__(
        self,
        pre_exp=None,
        act_energy=None,
        data_T: list = None,
        data_y: list = None,
        law: str = None,
        **kwargs,
    ) -> None:
        self.law = law
        super().__init__(
            pre_exp=pre_exp,
            act_energy=act_energy,
            data_T=data_T,
            data_y=data_y,
            **kwargs,
        )

    @property
    def law(self):
        return self._law

    @law.setter
    def law(self, value):
        acceptable_values = ["sievert", "henry", None]
        if value not in acceptable_values:
            raise ValueError(f"law should be one of {acceptable_values}, not {value}")
        self._law = value

    @ArrheniusProperty.pre_exp.setter
    def pre_exp(self, value):
        if value is None:
            self._pre_exp = value
            return
        if isinstance(value, pint.Quantity):
            self.set_law_from_quantity(value)

            self._pre_exp = value.to(self.units)
        elif self.law is None:
            raise ValueError(
                "units are required for Permeability.pre_exp, set law argument for default units"
            )
        else:
            warnings.warn(
                f"no units were given with pre-exponential factor, assuming {self.units:~}"
            )
            self._pre_exp = value * self.units

    @ArrheniusProperty.data_y.setter
    def data_y(self, value):
        if value is None:
            self._data_y = value
            return
        if isinstance(value, pint.Quantity):
            self.set_law_from_quantity(value)

            # convert to right units
            value = value.to(self.units)
        else:
            raise ValueError("units are required for Permeability")
        value = self._remove_nan_in_experimental_points(value)

        self._data_y = value

    def set_law_from_quantity(self, quantity):
        sievert_units = (
            ureg.particle * ureg.meter**-1 * ureg.second**-1 * ureg.Pa**-0.5
        )
        henry_units = (
            ureg.particle * ureg.meter**-1 * ureg.second**-1 * ureg.Pa**-1
        )
        if quantity.check(sievert_units):
            self.law = "sievert"
        elif quantity.check(henry_units):
            self.law = "henry"
        else:
            raise ValueError(
                f"Wrong dimensionality for permeability. Should be one of {[henry_units.dimensionality, sievert_units.dimensionality]}"
            )

    @property
    def units(self):
        if self.law == "sievert":
            return (
                ureg.particle * ureg.meter**-1 * ureg.second**-1 * ureg.Pa**-0.5
            )
        elif self.law == "henry":
            return ureg.particle * ureg.meter**-1 * ureg.second**-1 * ureg.Pa**-1


class RecombinationCoeff(ArrheniusProperty):
    """RecombinationCoeff class"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def units(self):
        return ureg.particle * ureg.meter**4 * ureg.second**-1 * ureg.particle**-2


class DissociationCoeff(ArrheniusProperty):
    """DissociationCoeff class"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def units(self):
        return ureg.particle * ureg.meter**-2 * ureg.s**-1 * ureg.Pa**-1


def get_nb_citations(doi: str):
    """Returns the number of citations of a given doi in the crossref database

    Args:
        doi (str): the DOI of the source

    Returns:
        int: the number of citations according to crossref
    """
    record = works.doi(doi)
    if record:
        nb_citations = record["is-referenced-by-count"]
    else:
        nb_citations = 0
    return nb_citations


my_etiquette = Etiquette(
    "H-transport-materials",
    "latest",
    "https://github.com/RemDelaporteMathurin/h-transport-materials",
    "rdelaportemathurin@gmail.com",
)

works = Works(etiquette=my_etiquette)
