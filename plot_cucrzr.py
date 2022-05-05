from h_transport_materials import *
from h_transport_materials.plotting import *
import matplotx
import matplotlib.pyplot as plt

with plt.style.context(matplotx.styles.dufte):

    fig, axs = plt.subplots(2, 1, figsize=(6.4, 6.6), sharex=True)
    plt.sca(axs[0])
    plt.yscale("log")

    plot(serra_diffusivity_h)
    plot(serra_diffusivity_d)
    plot(penalva_diffusivity_cucrzr_h)
    plot(nog_diffusivity_cucrzr_t)
    plot(anderl_diffusivity_cucrzr_d)

    line_labels(fontsize=10)
    plt.xlabel("")
    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")

    plt.sca(axs[1])
    plt.yscale("log")

    plot(serra_solubility_h)
    plot(serra_solubility_d)
    plot(penalva_solubility_cucrzr_h)
    plot(nog_solubility_cucrzr_t_1)
    # plot(nog_solubility_cucrzr_t_2)

    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")
    line_labels(fontsize=10)
    plt.ylim(bottom=7e19)
    plt.tight_layout()
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.show()
