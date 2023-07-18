import matplotlib.pyplot as plt
import numpy as np
import pint
from h_transport_materials import (
    Property,
    PropertiesGroup,
    ureg,
    Solubility,
    Diffusivity,
    Permeability,
    RecombinationCoeff,
    DissociationCoeff,
)
from typing import Union
import warnings


def plot(
    prop: Union[Property, PropertiesGroup],
    T_bounds=(300, 1200),
    inverse_temperature=True,
    auto_label=True,
    show_datapoints=True,
    scatter_kwargs={},
    colour_by="property",
    key_to_colour=None,
    **kwargs,
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
        key_to_colour (dict, optional): a dictionary with keys (eg. material)
            corresponding to colours. Defaults to None
        kwargs: other matplotlib.pyplot.plot arguments
    Returns:
        matplotlib.lines.Line2D: the Line2D artist
    """
    if isinstance(prop, Property):
        return _plot_property(
            prop,
            T_bounds,
            inverse_temperature,
            auto_label,
            show_datapoints,
            scatter_kwargs,
            **kwargs,
        )
    elif isinstance(prop, PropertiesGroup):
        group = prop
        if prop.units == "mixed units":
            raise ValueError("Cannot plot group with mixed units")

        # compute the prop to colour mapping
        if colour_by != "property":
            prop_to_color = get_prop_to_color(
                group,
                colour_by,
                key_to_colour,
                colour_cycle=plt.rcParams["axes.prop_cycle"].by_key()["color"],
            )
        elif key_to_colour is not None:
            warnings.warn(
                UserWarning(
                    "key_to_colour specified with colour_by='property' will be ignored"
                )
            )

        lines = []
        for single_prop in group:
            # change colour from kwargs if need be
            current_kwargs = kwargs.copy()
            if colour_by != "property" and "color" not in kwargs:
                current_kwargs["color"] = prop_to_color[single_prop]

            # change the label based on colour_by
            current_kwargs["label"] = _label_from_colour_by(single_prop, colour_by)

            l = _plot_property(
                single_prop,
                T_bounds=T_bounds,
                inverse_temperature=inverse_temperature,
                auto_label=auto_label,
                show_datapoints=show_datapoints,
                scatter_kwargs=scatter_kwargs,
                **current_kwargs,
            )
            lines.append(l)
        legend()
        return lines


def _plot_property(
    prop: Property,
    T_bounds=(300, 1200),
    inverse_temperature=True,
    auto_label=True,
    show_datapoints=True,
    scatter_kwargs={},
    **kwargs,
):
    """Plots a Property object on a temperature plot

    Args:
        prop (Property): the property (or group of properties)
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
        kwargs: other matplotlib.pyplot.plot arguments
    Returns:
        matplotlib.lines.Line2D: the Line2D artist
    """
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


def get_prop_to_color(
    group: PropertiesGroup,
    colour_by: str,
    key_to_colour: dict = None,
    colour_cycle: list = None,
):
    """Returns a dictionary mapping Property objects to a colour based on
    a property attribute

    Args:
        group (PropertiesGroup): a group of properties
        colour_by (str): a property attribute to colour by (eg. "author", "isotope", "material")
        key_to_colour (dict, optional): a dictionary with keys (eg. material)
            corresponding to colours. Defaults to None
        colour_cycle (list, optional): a list of colours used if colour_by is key_to_colour is not given

    Returns:
        dict: a dictionary mapping properties to colours
    """

    if colour_by == "property":
        assert colour_cycle is not None
        prop_to_colour = {
            prop: colour_cycle[i % len(colour_cycle)] for i, prop in enumerate(group)
        }
        return prop_to_colour

    all_keys = list(set([getattr(prop, colour_by) for prop in group]))
    if not key_to_colour:  # if key_to_colour not specified, use colour_cycle
        assert colour_cycle is not None
        key_to_colour = {
            key: colour_cycle[i % len(colour_cycle)] for i, key in enumerate(all_keys)
        }
    prop_to_colour = {prop: key_to_colour[getattr(prop, colour_by)] for prop in group}

    return prop_to_colour


def plot_plotly(
    group_of_properties: PropertiesGroup,
    T_bounds=(300, 1200),
    colour_by="property",
    show_datapoints=True,
    line_kwargs={},
    scatter_kwargs={},
):
    """Creates a plotly graph for visualising properties.

    Args:
        group_of_properties (list): a group of properties
        T_bounds (tuple, optional): If the property doesn't have
            a temperature range, this range will be used. Defaults
            to (300, 1200).
        colour_by (str, optional): "property", "material", "isotope", "author".
            Defaults to "property".
        show_datapoints (bool, optional): If True, the experimental datapoints will be
            scattered too. Defaults to True.
        line_kwargs (dict, optional): the keywords args for `line`. Defaults to {}.
        scatter_kwargs (dict, optional): the keywords args for `marker`. Defaults to {}.

    Returns:
        go.Figure: the graph
    """
    import plotly.graph_objects as go

    colour_cycle = [
        "#636EFA",
        "#EF553B",
        "#00CC96",
        "#AB63FA",
        "#FFA15A",
        "#19D3F3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52",
    ]
    prop_to_color = get_prop_to_color(
        group_of_properties, colour_by, colour_cycle=colour_cycle
    )

    fig = go.Figure()
    for prop in group_of_properties:
        line_kwargs["color"] = prop_to_color[prop]

        _plot_property_plotly(
            prop,
            fig,
            line_kwargs,
            scatter_kwargs=scatter_kwargs,
            T_bounds=T_bounds,
            show_datapoints=show_datapoints,
        )

    _update_axes(fig, group_of_properties)
    return fig


def _plot_property_plotly(
    prop,
    fig,
    line_kwargs,
    scatter_kwargs={},
    T_bounds=(300, 1200),
    show_datapoints=True,
):
    """Adds a property line and points to a current plotly figure

    Args:
        prop (_type_): _description_
        fig (_type_): _description_
        line_kwargs (dict): _description_
        scatter_kwargs (dict, optional): _description_
        T_bounds (tuple, optional): If the property doesn't have
            a temperature range, this range will be used. Defaults
            to (300, 1200).
        show_datapoints (bool, optional): If True, the experimental datapoints will be
            scattered too. Defaults to True.
    """
    import plotly.graph_objects as go

    label = f"{prop.isotope} {prop.author.capitalize()} ({prop.year})"
    if prop.range is None:
        range = T_bounds
    else:
        range = prop.range
    T = np.linspace(*range, num=500)
    if not isinstance(T, pint.Quantity):
        T *= ureg.K

    fig.add_trace(
        go.Scatter(
            x=1 / T.magnitude,
            y=prop.value(T).magnitude,
            name=label,
            mode="lines",
            line=line_kwargs,
            text=[label] * len(T),
            customdata=T.magnitude,
            hovertemplate=_make_hovertemplate(prop),
        )
    )

    if prop.data_T is not None and show_datapoints:
        scatter_kwargs["color"] = fig.data[-1].line.color
        fig.add_trace(
            go.Scatter(
                x=1 / prop.data_T.magnitude,
                y=prop.data_y.magnitude,
                name=label,
                mode="markers",
                marker=scatter_kwargs,
            )
        )


def _make_hovertemplate(prop):
    # TODO refactor this
    if isinstance(prop, Solubility):
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "S: %{y:,.2e} "
            + f"{prop.units:~H}<br>"
            + f"S_0: {prop.pre_exp:.2e~H} <br>"
            + f"E_S : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )
    elif isinstance(prop, Diffusivity):
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "D: %{y:,.2e} "
            + f"{prop.units:~H} <br>"
            + f"D_0: {prop.pre_exp:.2e~H}<br>"
            + f"E_D : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )
    else:
        return (
            "<b>%{text}</b><br><br>"
            + prop.material.name
            + "<br>"
            + "1/T: %{x:,.2e} K<sup>-1</sup><br>"
            + "T: %{customdata:.0f} K<br>"
            + "value: %{y:,.2e} "
            + f"{prop.units:~H} <br>"
            + f"pre-exp: {prop.pre_exp:.2e~H}<br>"
            + f"act. energy : {prop.act_energy:.2f~H}"
            + "<extra></extra>"
        )


def _update_axes(fig, group_of_properties):
    if len(group_of_properties) == 0:
        return

    if isinstance(group_of_properties[0], Solubility):
        all_units = np.unique([f"{S.units:~H}" for S in group_of_properties]).tolist()
        if len(all_units) == 1:
            yticks_suffix = all_units[0].replace("particle", " H")
            title_units = f"({yticks_suffix})"
        else:
            # if the group contains mixed units, display nothing
            title_units = "(mixed units)"
            yticks_suffix = ""
        ylabel = f"Solubility {title_units}"
    elif isinstance(group_of_properties[0], Diffusivity):
        ylabel = "Diffusivity"
        yticks_suffix = f" {group_of_properties[0].units:~H}"
    elif isinstance(group_of_properties[0], Permeability):
        ylabel = f"Permeability {group_of_properties[0].units:~H}"
        yticks_suffix = ""
    elif isinstance(group_of_properties[0], RecombinationCoeff):
        ylabel = "Recombination coefficient"
        yticks_suffix = " m<sup>4</sup>/s"
    elif isinstance(group_of_properties[0], DissociationCoeff):
        ylabel = f"Dissociation coefficient {group_of_properties[0].units:~H}"
        yticks_suffix = ""

    xticks_suffix = " K<sup>-1</sup>"

    fig.update_yaxes(
        title_text=ylabel, type="log", tickformat=".0e", ticksuffix=yticks_suffix
    )
    fig.update_xaxes(title_text="1/T", tickformat=".2e", ticksuffix=xticks_suffix)


def _label_from_colour_by(prop, colour_by):
    """Returns a label for a property based on a colour_by setting

    Args:
        prop (htm.Property): the property to label
        colour_by (str): a property attribute to colour by (eg. "author", "isotope", "material")

    Returns:
        str: the property label
    """
    if colour_by == "property":
        return f"{prop.isotope} {prop.author.capitalize()} ({prop.year})"
    elif colour_by == "material":
        return f"{prop.material}"
    elif colour_by == "author":
        return f"{prop.author.capitalize()}"
    elif colour_by == "isotope":
        return f"{prop.isotope}"


def legend(**kwargs):
    """Adds a legend to an existing plot.
    Should be used in combination with htm.plotting.plot(PropertiesGroup)
    """
    all_lines = plt.gca().get_lines()
    all_labels = [l.get_label() for l in all_lines]

    unique_labels = np.unique(all_labels)
    unique_lines = [all_lines[all_labels.index(label)] for label in unique_labels]

    plt.gca().legend(unique_lines, unique_labels, **kwargs)
