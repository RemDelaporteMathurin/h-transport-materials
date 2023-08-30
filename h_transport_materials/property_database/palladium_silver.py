import h_transport_materials as htm
from h_transport_materials import (
    Permeability,
    Diffusivity,
    Solubility,
    DissociationCoeff,
    RecombinationCoeff,
) 

u = htm.ureg

serra_permeability_h = Permeability(
    pre_exp=5.58e-8 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=6304 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="H",
    source="serra_hydrogen_1998-2",
    note="Figure 2 or Equation 6",
)

serra_permeability_d = Permeability(
    pre_exp=3.43e-8 * u.mol * u.m**-1 * u.Pa**-0.5 * u.s**-1,
    act_energy=6156 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="D",
    source="serra_hydrogen_1998-2",
    note="Figure 2 or Equation 7",
)

serra_diffusivity_h = Diffusivity(
    D_0=3.07e-7 * u.m**2 * u.s**-1,
    E_D=25902 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="H",
    source="serra_hydrogen_1998-2",
    note="Figure 3 or Equation 6",
)

serra_diffusivity_d = Diffusivity(
    D_0=1.87e-7 * u.m**2 * u.s**-1,
    E_D=24685 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="D",
    source="serra_hydrogen_1998-2",
    note="Figure 3 or Equation 7",
)

serra_solubility_h = Solubility(
    S_0=0.182 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-19598 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="H",
    source="serra_hydrogen_1998-2",
    note="Figure 4 or Equation 6",
)

serra_solubility_d = Solubility(
    S_0=0.184 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-18531 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="D",
    source="serra_hydrogen_1998-2",
    note="Figure 4 or Equation 7",
)

serra_dissociation_h = DissociationCoeff(
    pre_exp=1.7e-2 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=26294 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="H",
    source="serra_hydrogen_1998-2",
    note="Equation 8",
)

serra_dissociation_d = DissociationCoeff(
    pre_exp=1.3e-2 * u.mol * u.m**-2 * u.s**-1 * u.Pa**-1,
    act_energy=24780 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="D",
    source="serra_hydrogen_1998-2",
    note="Equation 9",
)

serra_recombination_h = RecombinationCoeff(
    pre_exp=0.51 * u.m**4 * u.s**-1 * u.mol**-1,
    act_energy=65490 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="H",
    source="serra_hydrogen_1998-2",
    note="Equation 8",
)

serra_recombination_d = RecombinationCoeff(
    pre_exp=0.39 * u.m**4 * u.s**-1 * u.mol**-1,
    act_energy=61842 * u.J * u.mol**-1,
    range=(373 * u.K, 773 * u.K),
    isotope="D",
    source="serra_hydrogen_1998-2",
    note="Equation 9",
)

properties = [
    serra_permeability_h,
    serra_permeability_d,
    serra_diffusivity_h,
    serra_diffusivity_d,
    serra_solubility_h,
    serra_solubility_d,
    serra_dissociation_h,
    serra_dissociation_d,
    serra_recombination_h,
    serra_recombination_d,
]

for prop in properties:
    prop.material = htm.PD25AG

htm.database += properties