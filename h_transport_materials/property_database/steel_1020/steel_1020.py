import h_transport_materials as htm
from h_transport_materials import Permeability, Solubility, Diffusivity
import numpy as np

u = htm.ureg

perm_data = np.genfromtxt(
    htm.absolute_path("gadgeel_1979_permeability.csv"),
    delimiter=",",
)

steel_1020_permeability_h = Permeability(
    data_T=1000 / (perm_data[:, 0] * u.K**-1),
    data_y=perm_data[:, 1] * u.ccNTP * u.cm**-1 * u.s**-1 * u.Pa**-0.5,
    source="gadgeel_gas-phase_1979",
    isotope="H",
    note="Figure 3; y-axis is cm3(NTP) H2 / cm / s / (N m^-2)^0.5",
)

sol_data = np.genfromtxt(
    htm.absolute_path("gadgeel_1979_solubility.csv"),
    delimiter=",",
)

# Gadgeel 1979 solubility was measured at 50 psi H2. The y-axis is
# concentration C (cm3 H2 / cm3 metal), not a Sieverts constant, so we divide
# by sqrt(P_exp) to convert to the Sieverts form htm.Solubility requires.
P_EXP = (50 * u.psi).to(u.Pa)

steel_1020_solubility_h = Solubility(
    data_T=1000 / (sol_data[:, 0] * u.K**-1),
    data_y=(sol_data[:, 1] * u.ccNTP * u.cm**-3) / P_EXP**0.5,
    source="gadgeel_gas-phase_1979",
    isotope="H",
    note=(
        "Figure 5; y-axis is C (cm3 H2 / cm3 metal) measured at 50 psi H2 "
        "(3.447e5 Pa). Divided by sqrt(P_exp) to convert concentration to "
        "Sieverts constant, which is the form htm.Solubility requires."
    ),
)

diff_data = np.genfromtxt(
    htm.absolute_path("gadgeel_1979_diffusivity.csv"),
    delimiter=",",
)

steel_1020_diffusivity_h = Diffusivity(
    data_T=1000 / (diff_data[:, 0] * u.K**-1),
    data_y=diff_data[:, 1] * u.cm**2 * u.s**-1,
    source="gadgeel_gas-phase_1979",
    isotope="H",
    note="Figure 4",
)

properties = [
    steel_1020_permeability_h,
    steel_1020_solubility_h,
    steel_1020_diffusivity_h,
]

for prop in properties:
    prop.material = htm.STEEL_1020

htm.database += properties
