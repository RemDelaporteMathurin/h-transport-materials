.. _examples:

Complete examples
=================


Basic example
-------------

.. plot::
   :include-source: true

    import h_transport_materials as htm

    import matplotlib.pyplot as plt

    u = htm.ureg

    D_1 = htm.Diffusivity(
       D_0=1 * u.m**2 * u.s**-1,
       E_D=0.2* u.eV * u.particle**-1,
    )

    D_2 = htm.Diffusivity(
       D_0=2 * u.cm**2 * u.s**-1,
       E_D=0.3* u.eV * u.particle**-1,
    )

    htm.plotting.plot(D_1, label="diffusivity 1")
    htm.plotting.plot(D_2, label="diffusivity 2")

    plt.yscale("log")
    plt.legend()
    plt.show()

Convert properties units
------------------------

.. testcode::

    import h_transport_materials as htm
    
    u = htm.ureg

    my_diffusivity = htm.Diffusivity(
        D_0=1e-9 * u.m**2 * u.s**-1,
        E_D=0.5 * u.eV * u.particle**-1
    )


    print(my_diffusivity.pre_exp.to(u.miles**2 * u.month**-1))
    # please don't do this...

    print(my_diffusivity.act_energy.to(u.kcal * u.mol**-1))


.. testoutput::

    1.0153714565349241e-09 mile ** 2 / month
    11.530273915309515 kilocalorie / mole

Accessing the internal database: basic
--------------------------------------

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt

    flinak_diffusivities = htm.diffusivities.filter(material=htm.FLINAK)

    htm.plotting.plot(flinak_diffusivities)

    plt.legend()
    plt.yscale("log")
    plt.show()

Accessing the internal database: ``colour_by``
---------------------------------------------

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt

    tungsten_diffusivities = htm.diffusivities.filter(material=htm.TUNGSTEN)

    fig, axs = plt.subplots(3, 1, sharey=True, sharex=True)

    plt.sca(axs[0])
    htm.plotting.plot(tungsten_diffusivities)

    plt.sca(axs[1])
    htm.plotting.plot(tungsten_diffusivities, colour_by="author")

    plt.sca(axs[2])
    htm.plotting.plot(tungsten_diffusivities, colour_by="isotope")

    plt.yscale("log")
    plt.show()


Accessing the internal database: advanced
-----------------------------------------

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt

    mat_to_colour = {
        htm.COPPER: "tab:orange",
        htm.CUCRZR: "tab:brown",
        htm.TUNGSTEN: "tab:grey",
    }

    fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(6.4, 8), sharex=True)

    # change the format of units in matplotlib
    htm.ureg.mpl_formatter = "{:~P}"

    for i, group in enumerate([htm.diffusivities, htm.solubilities, htm.permeabilities]):
        plt.sca(axs[i])
        filtered_group = group.filter(material=list(mat_to_colour.keys()))
        htm.plotting.plot(
            filtered_group, alpha=0.6, colour_by="material", key_to_colour=mat_to_colour
        )
        plt.yscale("log")
        plt.xlabel("")  # remove default xlabel

    axs[0].get_legend().remove()
    axs[1].get_legend().remove()

    axs[0].set_title("Diffusivity")
    axs[1].set_title("Solubility")
    axs[2].set_title("Permeability")

    plt.xlabel(f"Inverse temperature ({axs[-1].xaxis.get_units():~P})")
    plt.show()


Accessing the internal database: statistics
-------------------------------------------

.. plot::
   :include-source: true

    import h_transport_materials as htm
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import norm


    def plot_histogram(data):
        # plot histogram
        counts, bins, _ = plt.hist(data, alpha=0.7, edgecolor="tab:blue")

        # fit with Gaussian
        (mu_pre_exp, sigma_pre_exp) = norm.fit(data)
        x_axis = np.linspace(min(data), max(data))
        best_fit = norm.pdf(x_axis, mu_pre_exp, sigma_pre_exp)
        bin_width = np.diff(bins)[0]
        scaling_factor = sum(bin_width * counts)

        # plot best fit
        plt.plot(x_axis, scaling_factor * best_fit)


    fig, (axs_top, axs_bot) = plt.subplots(nrows=2, ncols=2, sharey=True, figsize=(6.4, 6))

    for i, group in enumerate([htm.diffusivities, htm.solubilities]):
        # filter Steel properties
        props = group.filter(material=htm.Steel)

        all_pre_exp = [np.log10(prop.pre_exp.magnitude) for prop in props]
        all_act_energy = [prop.act_energy.magnitude for prop in props]

        plt.sca(axs_top[i])
        plot_histogram(all_pre_exp)

        plt.sca(axs_bot[i])
        plot_histogram(all_act_energy)


    axs_top[0].set_title("Diffusivity")
    axs_top[1].set_title("Solubility")

    axs_top[0].set_ylabel("Number of properties")
    axs_bot[0].set_ylabel("Number of properties")

    axs_top[0].set_xlabel(f"log10 ( $D_0$ {htm.diffusivities[0].units:~P} ) ")
    axs_top[1].set_xlabel(f"log10 ( $S_0$ {htm.solubilities[0].units:~P} ) ")
    axs_bot[0].set_xlabel(f"$E_D$ (eV)")
    axs_bot[1].set_xlabel(f"$E_S$ (eV)")

    axs_bot[0].set_xlim(0, 0.6)
    axs_bot[1].set_xlim(0, 0.6)

    plt.tight_layout()
    plt.show()
