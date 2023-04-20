import h_transport_materials as htm
from h_transport_materials.property import (
    Diffusivity,
    RecombinationCoeff,
    Solubility,
    Permeability,
)
from pathlib import Path
import numpy as np

frauenfelder_src = "frauenfelder_solution_1969"
frauenfelder_diffusivity = Diffusivity(
    D_0=4.1e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.39 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(1100 * htm.ureg.K, 2400 * htm.ureg.K),
    source=frauenfelder_src,
    isotope="H",
)
frauenfelder_solubility = Solubility(
    S_0=1.87e24 * htm.ureg.particle * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=1.04 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(1100 * htm.ureg.K, 2400 * htm.ureg.K),
    source=frauenfelder_src,
    isotope="H",
)


liu_src = "liu_hydrogen_2014"
liu_diffusivity_tungsten = Diffusivity(
    D_0=5.13e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.21 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(200 * htm.ureg.K, 3000 * htm.ureg.K),
    source=liu_src,
    isotope="H",
)


heinola_src = "heinola_diffusion_2010"
heinola_diffusivity_tungsten = Diffusivity(
    D_0=5.2e-8 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.21 * htm.ureg.eV * htm.ureg.particle**-1,
    source=heinola_src,
    isotope="H",
)

johnson_src = "johnson_hydrogen_2010"
johnson_diffusivity_tungsten_h = Diffusivity(
    D_0=6.32e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.39 * htm.ureg.eV * htm.ureg.particle**-1,
    source=johnson_src,
    isotope="H",
)

johnson_diffusivity_tungsten_t = Diffusivity(
    D_0=5.16e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.40 * htm.ureg.eV * htm.ureg.particle**-1,
    source=johnson_src,
    isotope="T",
)


moore_diffusivity_tungsten_h = Diffusivity(
    data_T=[1783.0, 1890.0, 1960.0, 2045.0, 2175.0] * htm.ureg.K,
    data_y=np.array([6.45e-9, 1.26e-8, 1.81e-8, 3.01e-8, 5.15e-8])
    * htm.ureg.cm**2
    * htm.ureg.s**-1,
    source="moore_thermal_2004",
    isotope="H",
    note="data in table IV. Units are not given but on page 2651 the equation indiquates that D is in cm2/s",
)


zakharov_diffusivity_tungsten_h = Diffusivity(
    data_T=htm.ureg.Quantity(np.array([400, 600, 800, 1000, 1200]), htm.ureg.degC),
    data_y=np.array([6.43e-8, 4.22e-6, 5.99e-5, 3.67e-4, 1.38e-3])
    * htm.ureg.cm**2
    * htm.ureg.s**-1,
    source="zakharov_hydrogen_1975",
    isotope="H",
    note="the author gives activation energies in cal",
)

ryabchikov_diffusivity_tungsten_h = Diffusivity(
    D_0=8.1e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=82.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(1055 * htm.ureg.K, 1570 * htm.ureg.K),
    source="ryabchikov_notitle_1964",
    isotope="H",
)

esteban_src = "esteban_hydrogen_2001"
esteban_diffusivity_tungsten_h = Diffusivity(
    D_0=5.68e-10 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=9.3 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="H",
)

esteban_diffusivity_tungsten_d = Diffusivity(
    D_0=5.49e-10 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=10 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="D",
)

esteban_diffusivity_tungsten_t = Diffusivity(
    D_0=5.34e-10 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=11.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="T",
)


esteban_solubility_tungsten_h = Solubility(
    S_0=2.9e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=26.9 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="H",
)

esteban_solubility_tungsten_d = Solubility(
    S_0=0.75e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=28.7 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="D",
)

esteban_solubility_tungsten_t = Solubility(
    S_0=2.25e-2 * htm.ureg.mol * htm.ureg.m**-3 * htm.ureg.Pa**-0.5,
    E_S=27.8 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    source=esteban_src,
    isotope="T",
)

holzner_src = "holzner_solute_2020"
holzner_diffusivity_tungsten_h = Diffusivity(
    D_0=2.06e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.28 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(1600 * htm.ureg.K, 2600 * htm.ureg.K),
    source=holzner_src,
    isotope="H",
)
holzner_diffusivity_tungsten_d = Diffusivity(
    D_0=1.60e-3 * htm.ureg.cm**2 * htm.ureg.s**-1,
    E_D=0.28 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(1600 * htm.ureg.K, 2600 * htm.ureg.K),
    source=holzner_src,
    isotope="D",
)

fernandez_diffusivity_tungsten_h = Diffusivity(
    D_0=1.93e-7 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.20 * htm.ureg.eV * htm.ureg.particle**-1,
    range=(300 * htm.ureg.K, 1200 * htm.ureg.K),
    source="fernandez_hydrogen_2015",
    isotope="H",
)

anderl_recomb = RecombinationCoeff(
    pre_exp=3.2e-15 * htm.ureg.m**4 * htm.ureg.s**-1 * htm.ureg.particle**-1,
    act_energy=1.16 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    source="anderl_deuterium_1992",
)

frauenfelder_p_0 = (
    1.5e-3
    * htm.ureg.torr
    * htm.ureg.liter
    * htm.ureg.cm**-1
    * htm.ureg.s**-1
    * htm.ureg.torr**-0.5
)
frauenfelder_permeability = Permeability(
    pre_exp=frauenfelder_p_0 / (htm.Rg * 300 * htm.ureg.K),
    act_energy=31.5 * htm.ureg.kcal * htm.ureg.mol**-1,
    isotope="H",
    range=(
        htm.ureg.Quantity(1050, htm.ureg.degC),
        htm.ureg.Quantity(2400, htm.ureg.degC),
    ),
    source="frauenfelder_permeation_1968",
)

zakharov_permeability = Permeability(
    pre_exp=5.2e-3
    * htm.ureg.ccNTP
    * htm.ureg.cm
    * htm.ureg.cm**-2
    * htm.ureg.s**-1
    * htm.ureg.atm**-0.5,
    act_energy=25400 * htm.ureg.cal * htm.ureg.mol**-1,
    source="zakharov_hydrogen_1975",
    isotope="H",
    range=(
        htm.ureg.Quantity(400, htm.ureg.degC),
        htm.ureg.Quantity(1200, htm.ureg.degC),
    ),
    note="the author gives activation energies in cal",
)

esteban_permeability_h = Permeability(
    pre_exp=1.65e-11
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.Pa**-0.5
    * htm.ureg.s**-1,
    act_energy=36.2 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    isotope="H",
    source="esteban_hydrogen_2001",
)

esteban_permeability_d = Permeability(
    pre_exp=1.51e-11
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.Pa**-0.5
    * htm.ureg.s**-1,
    act_energy=38.7 * htm.ureg.kJ * htm.ureg.mol**-1,
    range=(673 * htm.ureg.K, 1073 * htm.ureg.K),
    isotope="D",
    source="esteban_hydrogen_2001",
)

# TODO fit this ourselves
zhao_permeability = Permeability(
    pre_exp=3.2e-8
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.Pa**-0.5
    * htm.ureg.s**-1,
    act_energy=0.81 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    range=(627 * htm.ureg.K, 965 * htm.ureg.K),
    source="zhao_deuterium_2020",
    note="undamaged W",
)

zhao_diffusivity = Diffusivity(
    D_0=3.0e-6 * htm.ureg.m**2 * htm.ureg.s**-1,
    E_D=0.64 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    range=(627 * htm.ureg.K, 965 * htm.ureg.K),
    source="zhao_deuterium_2020",
    note="undamaged W",
)


liang_permeability = Permeability(
    pre_exp=4.94e-7
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5,
    act_energy=1.38 * htm.ureg.eV * htm.ureg.particle**-1,
    isotope="D",
    range=(
        htm.ureg.Quantity(600, htm.ureg.degC),
        htm.ureg.Quantity(800, htm.ureg.degC),
    ),
    source="liang_deuterium_2018",
)


# LIU 2016 PAPER

liu_permeability_data = np.genfromtxt(
    str(Path(__file__).parent) + "/liu_2016/permeability.csv",
    delimiter=",",
    names=True,
)
liu_diffusivity_data = np.genfromtxt(
    str(Path(__file__).parent) + "/liu_2016/diffusivity.csv",
    delimiter=",",
    names=True,
)

rolled_50um_data_invT = liu_permeability_data["rolled_50umX"] * htm.ureg.K**-1
rolled_50um_data_y = (
    liu_permeability_data["rolled_50umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_rolled_50um = Permeability(
    data_T=1 / rolled_50um_data_invT,
    data_y=rolled_50um_data_y,
    source="liu_gas-driven_2016",
    note="rolled_50um",
    isotope="H",
)

rolled_114um_data_invT = liu_permeability_data["rolled_114umX"] * htm.ureg.K**-1
rolled_114um_data_y = (
    liu_permeability_data["rolled_114umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_rolled_114um = Permeability(
    data_T=1 / rolled_114um_data_invT,
    data_y=rolled_114um_data_y,
    source="liu_gas-driven_2016",
    note="rolled_144um",
    isotope="H",
)

rolled_240um_data_invT = liu_permeability_data["rolled_240umX"] * htm.ureg.K**-1
rolled_240um_data_y = (
    liu_permeability_data["rolled_240umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_rolled_240um = Permeability(
    data_T=1 / rolled_240um_data_invT,
    data_y=rolled_240um_data_y,
    source="liu_gas-driven_2016",
    note="rolled_240um",
    isotope="H",
)

annealed_50um_data_invT = liu_permeability_data["annealed_50umX"] * htm.ureg.K**-1
annealed_50um_data_y = (
    liu_permeability_data["annealed_50umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_annealed_50um = Permeability(
    data_T=1 / annealed_50um_data_invT,
    data_y=annealed_50um_data_y,
    source="liu_gas-driven_2016",
    isotope="H",
    note="annealed_50um",
)

annealed_250um_data_invT = liu_permeability_data["annealed_250umX"] * htm.ureg.K**-1
annealed_250um_data_y = (
    liu_permeability_data["annealed_250umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_annealed_250um = Permeability(
    data_T=1 / annealed_250um_data_invT,
    data_y=annealed_250um_data_y,
    source="liu_gas-driven_2016",
    isotope="H",
    note="annealed_250um",
)

recrystallized_250um_data_invT = (
    liu_permeability_data["recrystallized_250umX"] * htm.ureg.K**-1
)
recrystallized_250um_data_y = (
    liu_permeability_data["recrystallized_250umY"]
    * htm.ureg.mol
    * htm.ureg.m**-1
    * htm.ureg.s**-1
    * htm.ureg.Pa**-0.5
)
liu_permeability_recrystallized_250um = Permeability(
    data_T=1 / recrystallized_250um_data_invT,
    data_y=recrystallized_250um_data_y,
    source="liu_gas-driven_2016",
    isotope="H",
    note="recrystallized_250um",
)


rolled_114um_data_invT = liu_diffusivity_data["rolled_114umX"] * htm.ureg.K**-1
rolled_114um_data_y = (
    liu_diffusivity_data["rolled_114umY"] * htm.ureg.m**2 * htm.ureg.s**-1
)
liu_diffusivity_rolled_114um = Diffusivity(
    data_T=1 / rolled_114um_data_invT,
    data_y=rolled_114um_data_y,
    source="liu_gas-driven_2016",
    note="rolled_144um",
    isotope="H",
)

rolled_240um_data_invT = liu_diffusivity_data["rolled_240umX"] * htm.ureg.K**-1
rolled_240um_data_y = (
    liu_diffusivity_data["rolled_240umY"] * htm.ureg.m**2 * htm.ureg.s**-1
)
liu_diffusivity_rolled_240um = Diffusivity(
    data_T=1 / rolled_240um_data_invT,
    data_y=rolled_240um_data_y,
    source="liu_gas-driven_2016",
    note="rolled_240um",
    isotope="H",
)

annealed_102um_data_invT = liu_diffusivity_data["annealed_102umX"] * htm.ureg.K**-1
annealed_102um_data_y = (
    liu_diffusivity_data["annealed_102umY"] * htm.ureg.m**2 * htm.ureg.s**-1
)
liu_diffusivity_annealed_102um = Diffusivity(
    data_T=1 / annealed_102um_data_invT,
    data_y=annealed_102um_data_y,
    source="liu_gas-driven_2016",
    note="annealed_102um",
    isotope="H",
)

annealed_250um_data_invT = liu_diffusivity_data["annealed_250umX"] * htm.ureg.K**-1
annealed_250um_data_y = (
    liu_diffusivity_data["annealed_250umY"] * htm.ureg.m**2 * htm.ureg.s**-1
)
liu_diffusivity_annealed_250um = Diffusivity(
    data_T=1 / annealed_250um_data_invT,
    data_y=annealed_250um_data_y,
    source="liu_gas-driven_2016",
    note="annealed_250um",
    isotope="H",
)


recrystallized_250um_data_invT = (
    liu_diffusivity_data["recrystallized_250umX"] * htm.ureg.K**-1
)
recrystallized_250um_data_y = (
    liu_diffusivity_data["recrystallized_250umY"] * htm.ureg.m**2 * htm.ureg.s**-1
)
liu_diffusivity_recrystallized_250um = Diffusivity(
    data_T=1 / recrystallized_250um_data_invT,
    data_y=recrystallized_250um_data_y,
    source="liu_gas-driven_2016",
    note="recrystallized_250um",
    isotope="H",
)


properties = [
    frauenfelder_diffusivity,
    liu_diffusivity_tungsten,
    heinola_diffusivity_tungsten,
    johnson_diffusivity_tungsten_h,
    johnson_diffusivity_tungsten_t,
    moore_diffusivity_tungsten_h,
    zakharov_diffusivity_tungsten_h,
    ryabchikov_diffusivity_tungsten_h,
    esteban_diffusivity_tungsten_h,
    esteban_diffusivity_tungsten_d,
    esteban_diffusivity_tungsten_t,
    holzner_diffusivity_tungsten_h,
    holzner_diffusivity_tungsten_d,
    fernandez_diffusivity_tungsten_h,
    frauenfelder_solubility,
    esteban_solubility_tungsten_h,
    esteban_solubility_tungsten_d,
    esteban_solubility_tungsten_t,
    anderl_recomb,
    frauenfelder_permeability,
    zakharov_permeability,
    esteban_permeability_h,
    esteban_permeability_d,
    zhao_permeability,
    zhao_diffusivity,
    liang_permeability,
    liu_permeability_rolled_50um,
    liu_permeability_rolled_114um,
    liu_permeability_rolled_240um,
    liu_permeability_annealed_50um,
    liu_permeability_annealed_250um,
    liu_permeability_recrystallized_250um,
    liu_diffusivity_rolled_114um,
    liu_diffusivity_rolled_240um,
    liu_diffusivity_annealed_102um,
    liu_diffusivity_annealed_250um,
    liu_diffusivity_recrystallized_250um,
]

for prop in properties:
    prop.material = htm.TUNGSTEN

htm.database += properties
