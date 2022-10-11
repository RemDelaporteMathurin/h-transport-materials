from typing import Iterable
import numpy as np
from crossref.restful import Works, Etiquette
from pybtex.database import BibliographyData, parse_string
from h_transport_materials import k_B, bib_database
from h_transport_materials.fitting import fit_arhenius

import warnings


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
        note: str = None,
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
            note (str, optional): additional information. Defaults to None.
        """

        self.material = material
        self.source = source
        self.name = name
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

    def value(self, T):
        pass


class ArrheniusProperty(Property):
    def __init__(
        self,
        pre_exp: float = None,
        act_energy: float = None,
        data_T: list = None,
        data_y: list = None,
        **kwargs,
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

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp}
        Activation energy: {self.act_energy} eV
        """
        return val

    @property
    def range(self):
        if self._range is None and self.data_T is not None:
            self.fit()
        return self._range

    @range.setter
    def range(self, value):
        self._range = value

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
            value_as_array = np.array(value)
            self._data_T = value_as_array[
                ~np.isnan(value_as_array)
            ]  # remove nan values
        else:
            self._data_T = value[~np.isnan(value)]

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
            value_as_array = np.array(value)
            self._data_y = value_as_array[
                ~np.isnan(value_as_array)
            ]  # remove nan values
        else:
            self._data_y = value[~np.isnan(value)]

    def fit(self):
        self.pre_exp, self.act_energy = fit_arhenius(self.data_y, self.data_T)
        self.range = (self.data_T.min(), self.data_T.max())

    def value(self, T, exp=np.exp):
        return self.pre_exp * exp(-self.act_energy / k_B / T)


class Solubility(ArrheniusProperty):
    """Solubility class

    Args:
        units (str): units of the solubility "m-3 Pa-1/2" or "m-3 Pa-1".
        S_0 (float, optional): pre-exponential factor. Defaults to None.
        E_S (float, optional): activation energy (eV). Defaults to None.
    """

    def __init__(
        self, units: str, S_0: float = None, E_S: float = None, **kwargs
    ) -> None:

        super().__init__(pre_exp=S_0, act_energy=E_S, **kwargs)
        self.units = units

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp} {self.units}
        Activation energy: {self.act_energy} eV
        """
        return val

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        acceptable_values = ["m-3 Pa-1/2", "m-3 Pa-1"]
        if value not in acceptable_values:
            raise ValueError(
                "units can only accept {} or {}".format(*acceptable_values)
            )
        self._units = value


class Diffusivity(ArrheniusProperty):
    """Diffusivity class

    Args:
        D_0 (float, optional): pre-exponential factor (m2/s). Defaults to None.
        E_D (float, optional): activation energy (eV). Defaults to None.
    """

    def __init__(self, D_0: float = None, E_D: float = None, **kwargs) -> None:
        super().__init__(pre_exp=D_0, act_energy=E_D, **kwargs)

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp} m2/s
        Activation energy: {self.act_energy} eV
        """
        return val


class Permeability(ArrheniusProperty):
    """Permeability class"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp} m-1 Pa-1/2 s-1
        Activation energy: {self.act_energy} eV
        """
        return val


class RecombinationCoeff(ArrheniusProperty):
    """RecombinationCoeff class"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp} m4/s
        Activation energy: {self.act_energy} eV
        """
        return val


class DissociationCoeff(ArrheniusProperty):
    """DissociationCoeff class"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self) -> str:
        val = f"""
        Author: {self.author.capitalize()}
        Material: {self.material}
        Year: {self.year}
        Isotope: {self.isotope}
        Pre-exponential factor: {self.pre_exp} m-3 Pa-1
        Activation energy: {self.act_energy} eV
        """
        return val


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
