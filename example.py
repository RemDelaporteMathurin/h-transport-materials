from h_transport_materials import *
from h_transport_materials.plotting import plot, line_labels
import matplotlib.pyplot as plt
import matplotx

grey_W = "tab:grey"
orange_Cu = (228/255, 146/255, 64/255)
yellow_CuCrZr = (180/255, 95/255, 6/255)

with plt.style.context(matplotx.styles.dufte):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.8, 6.5))

    plt.sca(axs[0])
    # tungsten
    plot(frauenfelder_diffusivity, color=grey_W)
    # plot(reiter_diffusivity_tungsten, color=grey_W, T_bounds=T_bounds_W)

    # copper
    plot(reiter_diffusivity_copper, color=orange_Cu)

    # cucrzr
    plot(serra_diffusivity_h, color=yellow_CuCrZr)

    plt.yscale("log")
    plt.xlabel("")
    # matplotx.line_labels()  # put labels on the right
    line_labels()
    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")

    plt.sca(axs[1])
    # tungsten
    plot(frauenfelder_solubility, color=grey_W)

    # copper
    plot(reiter_solubility, color=orange_Cu)

    # cucrzr
    plot(serra_solubility_h, color=yellow_CuCrZr)

    plt.yscale("log")

    l1, = plt.plot([], [], color=grey_W, label="Tungsten")
    l2, = plt.plot([], [], color=orange_Cu, label="Copper")
    l3, = plt.plot([], [], color=yellow_CuCrZr, label="CuCrZr")
    legend_lines = [l1, l2, l3]
    legend = plt.legend(legend_lines, [l.get_label() for l in legend_lines], loc="upper right")
    plt.gca().add_artist(legend)
    # matplotx.line_labels()  # put labels on the right
    line_labels()
    plt.ylim(top=1e23)
    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")
    plt.tight_layout()
    plt.show()
