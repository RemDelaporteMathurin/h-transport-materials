import h_transport_materials as htm
from h_transport_materials.plotting import *
import matplotx
import matplotlib.pyplot as plt

with plt.style.context(matplotx.styles.dufte):

    fig, axs = plt.subplots(2, 1, figsize=(6.4, 6.6), sharex=True)
    plt.sca(axs[0])
    plt.yscale("log")

    diffusivities = htm.diffusivities.filter(material="cucrzr")
    for property in diffusivities:
        plot(property)

    line_labels(fontsize=10)
    plt.xlabel("")
    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")

    plt.sca(axs[1])
    plt.yscale("log")

    solubilities = htm.solubilities.filter(material="cucrzr")
    for property in solubilities:
        plot(property)

    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")
    line_labels(fontsize=10)
    plt.ylim(bottom=7e19)
    plt.tight_layout()
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.show()
