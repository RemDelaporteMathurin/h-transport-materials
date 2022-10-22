import numpy as np
import json
from pybtex.database import BibliographyData

from h_transport_materials.fitting import fit_arhenius


class PropertiesGroup(list):
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
        """Returns properties that match the specified arguments.
        Usage:
        ```
        group = htm.diffusivities

        # filter tungsten and authors esteban or heinola
        filtered_props = group.filter(material="tungsten").filter(author=["esteban", "heinola"])

        # exclude isotope T
        filtered_props = filtered_props.filter(exclude=True, isotope="T")

        property = filtered_props[0]
        ```

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

        return filtered_props

    def mean(self, samples_per_line=5, default_range=(300, 1200)):
        """Fits all the data and returns the mean pre-exponential
        factor and activation energy.

        Args:
            samples_per_line (int, optional): number of points taken
                per Property if it doesn't have any data. Defaults to 5.
            default_range (tuple, optional): temperature range taken if
                a Property doesn't have range. Defaults to (300, 1200).

        Returns:
            float, float: pre-exponential factor, activation energy (eV)
        """
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
                prop_y = prop.value(prop_T)

            data_T = np.concatenate((data_T, prop_T))
            data_y = np.concatenate((data_y, prop_y))

        # fit all the data
        pre_exp, act_energy = fit_arhenius(data_y, data_T)

        return pre_exp, act_energy

    def export_bib(self, filename: str):
        """Exports the bibliography data

        Args:
            filename (str): the path of the exported file
        """

        self.bibdata.to_file(filename)

    def export_to_json(self, filename: str):
        keys = [
            "material",
            "pre_exp",
            "act_energy",
            "isotope",
            "author",
            "source",
            "range",
            "doi",
            "units",
        ]

        data = []
        for prop in self:

            prop_dict = {key: getattr(prop, key) for key in keys if hasattr(prop, key)}
            if "units" in prop_dict:
                prop_dict["units"] = f"{prop_dict['units']:~}"
            data.append(prop_dict)

        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)
