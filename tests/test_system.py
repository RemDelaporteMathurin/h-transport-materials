import h_transport_materials as htm

import pint


def test_that_groups_are_not_empty():
    for group in [htm.diffusivities, htm.solubilities, htm.recombination_coeffs]:
        assert len(group) > 0


def test_all_solubilities_are_solubility():
    for sol in htm.solubilities:
        assert isinstance(sol, htm.Solubility)


def test_all_diffusivities_are_diffusivity():
    for diff in htm.diffusivities:
        assert isinstance(diff, htm.Diffusivity)


def test_all_recomb_are_recombinationcoeff():
    for diff in htm.recombination_coeffs:
        assert isinstance(diff, htm.RecombinationCoeff)


def test_all_dissociations_are_dissociationncoeff():
    for diff in htm.dissociation_coeffs:
        assert isinstance(diff, htm.DissociationCoeff)


def test_all_properties_have_required_attributes():
    for prop in htm.database:
        assert prop.material
        assert isinstance(prop.pre_exp, pint.Quantity)
        assert isinstance(prop.act_energy, pint.Quantity)
        assert prop.isotope


def test_all_properties_have_references():
    for prop in htm.database:
        assert prop.author
        assert prop.year
        assert prop.source


def test_all_properties_have_reasonable_activation_energies():
    for prop in htm.database:
        print(prop)
        assert abs(prop.act_energy) < 4 * htm.ureg.eV * htm.ureg.particle**-1


def test_all_diffusivities_have_reasonable_pre_exp():
    """Checks that all the diffusivities have pre_exp factors below 100 m2/s"""
    for prop in htm.diffusivities:
        print(prop)
        assert abs(prop.pre_exp) < 100 * htm.ureg.m**2 * htm.ureg.s**-1
