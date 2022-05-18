import h_transport_materials as htm
from h_transport_materials.plotting import *
import matplotx
import matplotlib.pyplot as plt

T_bounds = (1000/1.5, 1000/0.7)

with plt.style.context(matplotx.styles.dufte):

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 6.6))
    plt.sca(axs[0])

    # plt.figure(figsize=(6.4, 3.3))
    plt.yscale("log")

    diffusivities = htm.diffusivities.filter(material="tungsten").filter(isotope="H")
    for property in diffusivities:
        plot(property)

    line_labels(fontsize=10)

    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
    plt.xlabel("")

    plt.sca(axs[1])
    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")
    solubilities = htm.solubilities.filter(material="tungsten").filter(isotope="H")
    for property in solubilities:
        plot(property)


    plt.yscale("log")
    line_labels(fontsize=10)

    plt.tight_layout()
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.show()
