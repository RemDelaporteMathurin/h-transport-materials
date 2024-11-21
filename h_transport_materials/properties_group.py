import numpy as np
import json
from pybtex.database import BibliographyData
import warnings
from textwrap import dedent

from h_transport_materials import ureg, ArrheniusProperty, __version__

warnings.filterwarnings("always", message="No property matching the requirements")


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

    def mean(self):
        """
        Returns the mean Arrhenius property.

        Raises:
            ValueError: When called on a mixed units group

        Returns:
            ArrheniusProperty: the mean arrhenius property
        """
        if self.units == "mixed units":
            raise ValueError("Can't compute mean on mixed units groups")

        # geometric mean of pre-exponential factor
        pre_exps = np.array([prop.pre_exp.magnitude for prop in self])
        scaling_factor = np.max(pre_exps)
        pre_exps = pre_exps / scaling_factor  # scale pre-exps to avoid inf

        pre_exp = pre_exps.prod() ** (1.0 / len(pre_exps))  # compute mean
        pre_exp = pre_exp * scaling_factor  # re-scale

        # arithmetic mean of activation energy
        act_energy = np.array([prop.act_energy.magnitude for prop in self]).mean()

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
        begin_tabular = r"\begin{tabular}{ c c c c}"
        end_tabular = r"\end{tabular}"
        end_center = r"\end{center}"

        # TODO expose the columns to the users

        header = f"""
                Material & pre-exp. factor & Act. energy & Reference \\\\"""
        core = [header]
        for prop in self:
            core.append(
                f"""
                {prop.material} & ${prop.pre_exp:.2e~L}$ & {prop.act_energy:.2f~P} & \cite{{{prop.source}}} \\\\"""
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
