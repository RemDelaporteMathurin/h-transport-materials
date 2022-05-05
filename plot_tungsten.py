from h_transport_materials import *
from h_transport_materials.plotting import *
import matplotx
import matplotlib.pyplot as plt

with plt.style.context(matplotx.styles.dufte):

    # plt.figure(figsize=(6.4, 3.3))
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 6.6), sharex=True)

    plt.sca(axs[0])
    plt.yscale("log")

    plot(liu_diffusivity_tungsten)
    plot(reiter_diffusivity_tungsten)
    plot(heinola_diffusivity_tungsten)

    plot(johnson_diffusivity_tungsten_h)
    plot(johnson_diffusivity_tungsten_t)
    plot(moore_diffusivity_tungsten_t)
    plot(zakharov_diffusivity_tungsten_h)
    plot(ryabchikov_diffusivity_tungsten_h)


    line_labels(fontsize=10)
    esteban_plot, = plot(esteban_diffusivity_tungsten_h)
    frauenfelder_plot, = plot(frauenfelder_diffusivity)

    plt.annotate(esteban_diffusivity_tungsten_h.name, (5.8e-4, 1.6e-11), fontsize=10, color=esteban_plot.get_color())
    plt.annotate(frauenfelder_diffusivity.name, (5e-4, 1.2e-7), fontsize=10, color=frauenfelder_plot.get_color())

    plt.xlabel("")
    plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
    plt.ylim(bottom=1e-15)

    plt.sca(axs[1])
    plot(frauenfelder_solubility, color=frauenfelder_plot.get_color())

    plot(esteban_solubility_tungsten_h, color=esteban_plot.get_color())
    plot(esteban_solubility_tungsten_d, color=esteban_plot.get_color())
    plot(esteban_solubility_tungsten_t, color=esteban_plot.get_color())

    plt.yscale("log")
    plt.ylim(bottom=1e19)
    line_labels(fontsize=10)
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
    plt.ylabel("Solubility (m$^{-3}$ Pa$^{-0.5}$)")

    plt.tight_layout()
    plt.show()
