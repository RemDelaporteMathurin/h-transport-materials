import matplotlib.pyplot as plt
import numpy as np
import pint
from h_transport_materials import Property, PropertiesGroup, ureg
from typing import Union


def plot(
    prop: Union[Property, PropertiesGroup],
    T_bounds=(300, 1200),
    inverse_temperature=True,
    auto_label=True,
    show_datapoints=True,
    scatter_kwargs={},
    colour_by="property",
    **kwargs
):
    """Plots a Property object on a temperature plot

    Args:
        prop (Property or PropertiesGroup): the property (or group of properties)
            to plot.
        T_bounds (tuple, optional): If the property doesn't have
            a temperature range, this range will be used. Defaults
            to (300, 1200).
        inverse_temperature (bool, optional): If True, the x axis
            will be the inverse temperature (in K^-1). Defaults to True.
        auto_label (bool, optional): If True, a label will be automatically
            generated from the isotope, author and year. Ignored if label is set in kwargs.
            Defaults to True.
        show_datapoints (bool, optional): If True, the experimental datapoints will be
            scattered too. Defaults to True.
        scatter_kwargs (dict, optional): other matplotlib.pyplot.scatter arguments.
            Defaults to {}.
        colour_by (str, optional): a property attribute to colour by (eg. "author", "isotope",
            "material"). Defaults to "property".
        kwargs: other matplotlib.pyplot.plot arguments
    Returns:
        matplotlib.lines.Line2D: the Line2D artist
    """
    if isinstance(prop, Property):
        return plot_property(
            prop,
            T_bounds,
            inverse_temperature,
            auto_label,
            show_datapoints,
            scatter_kwargs,
            **kwargs
        )
    elif isinstance(prop, PropertiesGroup):
        group = prop
        if prop.units == "mixed units":
            raise ValueError("Cannot plot group with mixed units")

        # compute the prop to colour mapping
        if colour_by != "property":
            prop_to_color = get_prop_to_color(group, colour_by)

        lines = []
        for single_prop in group:
            # change colour from kwargs if need be
            current_kwargs = kwargs.copy()
            if colour_by != "property" and "color" not in kwargs:
                current_kwargs["color"] = prop_to_color[single_prop]

            l = plot_property(
                single_prop,
                T_bounds=T_bounds,
                inverse_temperature=inverse_temperature,
                auto_label=auto_label,
                show_datapoints=show_datapoints,
                scatter_kwargs=scatter_kwargs,
                **current_kwargs
            )
            lines.append(l)
        return lines


def plot_property(
    prop: Property,
    T_bounds=(300, 1200),
    inverse_temperature=True,
    auto_label=True,
    show_datapoints=True,
    scatter_kwargs={},
    **kwargs
):
    if prop.range is None:
        range = T_bounds
    else:
        range = prop.range
    T = np.linspace(*range, num=50)
    if not isinstance(T, pint.Quantity):
        T *= ureg.K
    if inverse_temperature:
        plt.xlabel("1/T (K$^{-1}$)")
        x = (1 / T)[::-1]
        y = prop.value(T)[::-1]
    else:
        plt.xlabel("T (K)")
        x = T
        y = prop.value(T)

    if auto_label and "label" not in kwargs.keys():
        label = "{} {} ({})".format(prop.isotope, prop.author.capitalize(), prop.year)
        kwargs["label"] = label
    (l,) = plt.plot(x, y, **kwargs)
    if show_datapoints and prop.data_T is not None:
        if inverse_temperature:
            scat_x = (1 / prop.data_T)[::-1]
            scat_y = prop.data_y[::-1]
        else:
            scat_x = prop.data_T
            scat_y = prop.data_y
        if "alpha" not in scatter_kwargs:
            scatter_kwargs["alpha"] = l.get_alpha()
        plt.scatter(scat_x, scat_y, color=l.get_color(), **scatter_kwargs)
    return l


def get_prop_to_color(group: PropertiesGroup, colour_by: str):
    """Returns a dictionary mapping Property objects to a colour based on
    a property attribute

    Args:
        group (PropertiesGroup): a group of properties
        colour_by (str): a property attribute to colour by (eg. "author", "isotope", "material")

    Returns:
        dict: a dictionary mapping properties to colours
    """
    colour_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    all_keys = list(set([getattr(prop, colour_by) for prop in group]))
    key_to_colour = {
        key: colour_cycle[i % len(colour_cycle)] for i, key in enumerate(all_keys)
    }
    prop_to_colour = {prop: key_to_colour[getattr(prop, colour_by)] for prop in group}

    return prop_to_colour
