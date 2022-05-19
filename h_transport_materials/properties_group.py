import numpy as np

from h_transport_materials.fitting import fit_arhenius


class PropertiesGroup:
    def __init__(self) -> None:
        self.properties = []

    def __getitem__(self, item):
        return self.properties[item]

    def filter(self, exclude=False, **kwargs):
        """_summary_

        Args:
            exclude (bool, optional): if True, the searched
                keys will be excluded. Defaults to False.

        Returns:
            PropertiesGroup: _description_
        """
        list_of_props = PropertiesGroup()
        list_of_searched_props = self.properties
        for prop in list_of_searched_props:
            match = True
            for key, value in kwargs.items():
                if getattr(prop, key) != value:
                    match = False

            if (match and not exclude) or (not match and exclude):
                list_of_props.properties.append(prop)

        return list_of_props

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
        for prop in self.properties:
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
