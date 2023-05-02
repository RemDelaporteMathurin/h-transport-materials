import numpy as np
import json
from pybtex.database import BibliographyData
import pint
import warnings
from textwrap import dedent

from h_transport_materials.fitting import fit_arhenius
from h_transport_materials import ureg, ArrheniusProperty, __version__


class PropertiesGroup(list):
    @property
    def units(self):
        all_units = list(set([prop.units for prop in self]))
        if len(all_units) == 1:
            return all_units[0]
        else:
            return "mixed units"

    @property
    def bibdata(self):
        bibdata = {}

        for prop in self:
            if prop.bibsource is None:
                print("{} is not a bibsource".format(prop.source))
                continue
            key = prop.bibsource.key
            bibdata[key] = prop.bibsource

        return BibliographyData(bibdata)

    def filter(self, exclude=False, **kwargs):
        """
        Returns properties that match the specified arguments.
        Usage::

            group = htm.diffusivities

            # filter tungsten and authors esteban or heinola
            filtered_props = group.filter(material="tungsten").filter(author=["esteban", "heinola"])

            # exclude isotope T
            filtered_props = filtered_props.filter(exclude=True, isotope="T")

            my_prop = filtered_props[0]

        Args:
            exclude (bool, optional): if True, the searched
                keys will be excluded. Defaults to False.
            kwargs: attributes of properties (ex: material="tungsten").
                String values must be lowercase to ensure good comparison.

        Returns:
            PropertiesGroup: the resulting properties

        """
        filtered_props = PropertiesGroup()

        # iterate through properties
        for prop in self:
            match = True
            for attr, value in kwargs.items():
                prop_attr = getattr(prop, attr)

                if isinstance(prop_attr, str):
                    # make sure prop_attr are lower
                    prop_attr = prop_attr.lower()

                if isinstance(value, list):
                    if prop_attr not in value:
                        match = False
                elif prop_attr != value:
                    match = False

            # append the property to the filtered list
            if (match and not exclude) or (not match and exclude):
                filtered_props.append(prop)
        if len(filtered_props) == 0:
            warnings.warn("No property matching the requirements")
        return filtered_props

    def mean(self, samples_per_line=5, default_range=(300, 1200)):
        """
        Fits all the data and returns the mean pre-exponential
        factor and activation energy.

        Args:
            samples_per_line (int, optional): number of points taken
                per Property if it doesn't have any data. Defaults to 5.
            default_range (tuple, optional): temperature range taken if
                a Property doesn't have range. Defaults to (300, 1200).

        Raises:
            ValueError: When called on a mixed units group

        Returns:
            ArrheniusProperty: the mean arrhenius property
        """
        if self.units == "mixed units":
            raise ValueError("Can't compute mean on mixed units groups")

        # initialise data points
        data_T = np.array([])
        data_y = np.array([])

        # add data points
        for prop in self:
            # if the property has data points, use them
            if prop.data_T is not None:
                prop_T = prop.data_T
                prop_y = prop.data_y
            # else, take samples
            else:
                T_range = prop.range
                if prop.range == None:
                    T_range = default_range
                prop_T = np.linspace(T_range[0], T_range[1], num=samples_per_line)
                if not isinstance(prop_T, pint.Quantity):
                    prop_T = ureg.Quantity(prop_T, ureg.K)
                prop_y = prop.value(prop_T)

            data_T = np.concatenate((data_T, prop_T))
            data_y = np.concatenate((data_y, prop_y))

        # fit all the data
        pre_exp, act_energy = fit_arhenius(data_y, data_T)

        property = ArrheniusProperty(
            pre_exp * self.units, act_energy * ureg.eV * ureg.particle**-1
        )
        return property

    def export_bib(self, filename: str):
        """
        Exports the bibliography data

        Args:
            filename (str): the path of the exported file
        """

        self.bibdata.to_file(filename)

    def export_to_json(self, filename: str):
        data = {"data": []}
        for prop in self:
            data["data"].append(prop.to_json())

        data["htm_version"] = __version__

        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def to_latex_table(self):
        """Exports to simple latex table"""
        begin_center = r"\begin{center}"
        begin_tabular = r"\begin{tabular}{ c c c }"
        end_tabular = r"\end{tabular}"
        end_center = r"\end{center}"

        # TODO expose the columns to the users

        header = f"""
                Material & pre-exp. factor & Act. energy \\\\"""
        core = [header]
        for prop in self:
            core.append(
                f"""
                {prop.material} & ${prop.pre_exp:.2e~L}$ & {prop.act_energy:.2f~P} \\\\"""
            )

        latex_table = f"""
        {begin_center}
            {begin_tabular}
            {''.join(core)}
            {end_tabular}
        {end_center}
        """

        latex_table = dedent(latex_table).strip("\n")
        return latex_table
