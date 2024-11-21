import h_transport_materials as htm
from h_transport_materials import Diffusivity

u = htm.ureg

zhou_diffusivity_chromium_h_model1 = Diffusivity(
    D_0=1.680e-7 * u.m**2 * u.s**-1,
    E_D=0.0994 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="H",
    note="Table 2. Model 1 considering only hydrogen isotope vibrations",
)

zhou_diffusivity_chromium_h_model4 = Diffusivity(
    D_0=1.366e-7 * u.m**2 * u.s**-1,
    E_D=0.0998 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="H",
    note=(
        "Table 2. Model 4 considering lattice pDOS coupled "
        "with hydrogen isotope vibrations and thermal expansion"
    ),
)

zhou_diffusivity_chromium_d_model1 = Diffusivity(
    D_0=1.383e-7 * u.m**2 * u.s**-1,
    E_D=0.111 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="D",
    note="Table S2 of suplementary materials. Model 1 considering only hydrogen isotope vibrations",
)

zhou_diffusivity_chromium_d_model4 = Diffusivity(
    D_0=1.110e-7 * u.m**2 * u.s**-1,
    E_D=0.110 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="D",
    note=(
        "Table S2 of suplementary materials. Model 4 considering lattice pDOS coupled "
        "with hydrogen isotope vibrations and thermal expansion"
    ),
)

zhou_diffusivity_chromium_t_model1 = Diffusivity(
    D_0=1.204e-7 * u.m**2 * u.s**-1,
    E_D=0.114 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="T",
    note="Table S2 of suplementary materials. Model 1 considering only hydrogen isotope vibrations",
)

zhou_diffusivity_chromium_t_model4 = Diffusivity(
    D_0=9.539e-8 * u.m**2 * u.s**-1,
    E_D=0.114 * u.eV * u.particle**-1,
    range=(297 * u.K, 1000 * u.K),
    source="zhou_thermal_2024",
    isotope="T",
    note=(
        "Table S2 of suplementary materials. Model 4 considering lattice pDOS coupled "
        "with hydrogen isotope vibrations and thermal expansion"
    ),
)

properties = [
    zhou_diffusivity_chromium_h_model1,
    zhou_diffusivity_chromium_h_model4,
    zhou_diffusivity_chromium_d_model1,
    zhou_diffusivity_chromium_d_model4,
    zhou_diffusivity_chromium_t_model1,
    zhou_diffusivity_chromium_t_model4,
]

for prop in properties:
    prop.material = htm.CHROMIUM

htm.database += properties
