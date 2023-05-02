import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike
import pint
from h_transport_materials import Property, PropertiesGroup, ureg
import math
import matplotlib as mpl
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


def line_labels(
    ax=None,
    min_label_distance: float or str = "auto",
    alpha: float = 1.0,
    **text_kwargs
):
    """Adapted from matplotx"""
    ax = ax or plt.gca()

    logy = ax.get_yscale() == "log"
    logx = ax.get_xscale() == "log"

    if min_label_distance == "auto":
        # Make sure that the distance is alpha * fontsize. This needs to be translated
        # into axes units.
        fig = plt.gcf()
        fig_height_inches = fig.get_size_inches()[1]
        ax = plt.gca()
        ax_pos = ax.get_position()
        ax_height = ax_pos.y1 - ax_pos.y0
        ax_height_inches = ax_height * fig_height_inches
        ylim = ax.get_ylim()
        if logy:
            ax_height_ylim = math.log10(ylim[1]) - math.log10(ylim[0])
        else:
            ax_height_ylim = ylim[1] - ylim[0]
        # 1 pt = 1/72 in
        fontsize = mpl.rcParams["font.size"]
        assert fontsize is not None
        min_label_distance_inches = fontsize / 72 * alpha
        min_label_distance = (
            min_label_distance_inches / ax_height_inches * ax_height_ylim
        )

    # find all Line2D objects with a valid label and valid data
    lines = [
        child
        for child in ax.get_children()
        # https://stackoverflow.com/q/64358117/353337
        if (
            isinstance(child, mpl.lines.Line2D)
            and child.get_label()[0] != "_"
            and not np.all(np.isnan(child.get_ydata()))
        )
    ]

    if len(lines) == 0:
        return

    # Add "legend" entries.
    # Get last non-nan y-value.
    targets, targets_x = [], []
    for line in lines:
        ydata = line.get_ydata()
        xdata = line.get_xdata()
        targets.append(ydata[~np.isnan(ydata)][-1])
        targets_x.append(xdata[~np.isnan(xdata)][-1])

    if logy:
        targets = [math.log10(t) for t in targets]

    if logx:
        targets_x = [math.log10(t) for t in targets_x]

    # Sometimes, the max value if beyond ymax. It'd be cool if in this case we could put
    # the label above the graph (instead of the to the right), but for now let's just
    # cap the target y.
    ymax = ax.get_ylim()[1]
    targets = [min(target, ymax) for target in targets]

    targets = _move_min_distance(targets, min_label_distance)
    if logy:
        targets = [10**t for t in targets]
    # if logx:
    #     targets_x = [10**t for t in targets_x]

    labels = [line.get_label() for line in lines]
    colors = [line.get_color() for line in lines]

    # Leave the labels some space to breathe. If they are too close to the
    # lines, they can get visually merged.
    # <https://twitter.com/EdwardTufte/status/1416035189843714050>
    # Don't forget to transform to axis coordinates first. This makes sure the
    # https://stackoverflow.com/a/40475221/353337
    # axis_to_data = ax.transAxes + ax.transData.inverted()
    # xpos = axis_to_data.transform([1.03, 1.0])[0]
    for label, xpos, ypos, color in zip(labels, targets_x, targets, colors):
        plt.text(
            xpos, ypos, label, verticalalignment="center", color=color, **text_kwargs
        )


def _move_min_distance(targets: ArrayLike, min_distance: float) -> np.ndarray:
    """Move the targets such that they are close to their original positions, but keep
    min_distance apart.
    https://math.stackexchange.com/a/3705240/36678
    """
    # sort targets
    idx = np.argsort(targets)
    targets = np.sort(targets)

    n = len(targets)
    x0_min = targets[0] - n * min_distance
    A = np.tril(np.ones([n, n]))
    b = targets - (x0_min + np.arange(n) * min_distance)

    # import scipy.optimize
    # out, _ = scipy.optimize.nnls(A, b)

    out = nnls(A, b)

    sol = np.cumsum(out) + x0_min + np.arange(n) * min_distance

    # reorder
    idx2 = np.argsort(idx)
    return sol[idx2]


def nnls(A, b, eps: float = 1.0e-10, max_steps: int = 100):
    # non-negative least-squares after
    # <https://en.wikipedia.org/wiki/Non-negative_least_squares>
    A = np.asarray(A)
    b = np.asarray(b)

    AtA = A.T @ A
    Atb = A.T @ b

    m, n = A.shape
    assert m == b.shape[0]
    mask = np.zeros(n, dtype=bool)
    x = np.zeros(n)
    w = Atb
    s = np.zeros(n)
    k = 0
    while sum(mask) != n and max(w) > eps:
        if k >= max_steps:
            break
        mask[np.argmax(w)] = True

        s[mask] = np.linalg.lstsq(AtA[mask][:, mask], Atb[mask], rcond=None)[0]
        s[~mask] = 0.0

        while np.min(s[mask]) <= 0:
            alpha = np.min(x[mask] / (x[mask] - s[mask]))
            x += alpha * (s - x)
            mask[np.abs(x) < eps] = False

            s[mask] = np.linalg.lstsq(AtA[mask][:, mask], Atb[mask], rcond=None)[0]
            s[~mask] = 0.0

        x = s.copy()
        w = Atb - AtA @ x

        k += 1

    return x
