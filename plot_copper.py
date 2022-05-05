from h_transport_materials import *
from h_transport_materials.plotting import *
import matplotx
import matplotlib.pyplot as plt

T_bounds = (1000/1.5, 1000/0.7)

with plt.style.context(matplotx.styles.dufte):

    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 6.6))
    plt.sca(axs[0])

    # plt.figure(figsize=(6.4, 3.3))
    plt.yscale("log")

    plot(eichenauer_diffusivity_copper_h)
    plot(eichenauer_diffusivity_copper_d)
    plot(katz_diffusivity_copper_h, T_bounds=T_bounds)
    # plot(katz_diffusivity_copper_d, T_bounds=T_bounds)
    # plot(katz_diffusivity_copper_t, T_bounds=T_bounds)
    plot(magnusson_diffusivity_copper)
    plot(tanabe_diffusivity_copper_d)
    # plot(anderl_diffusivity_copper_d)
    plot(anderl_diffusivity_copper_d_1999)
    plot(sakamoto_diffusivity_copper_h)
    plot(otsuka_diffusivity_copper_t)
    plot(perkins_diffusivity_copper_h)

    line_labels(fontsize=10)

    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
    plt.xlabel("")

    plt.sca(axs[1])
    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")
    plot(eichenauer_solubility_copper_h)
    plot(eichenauer_solubility_copper_d)
    plot(reiter_solubility)
    plot(thomas_solubility_copper_h)
    plot(wampler_solubility_copper_h)

    plt.yscale("log")
    line_labels(fontsize=10)

    plt.tight_layout()
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.show()
