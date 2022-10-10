import h_transport_materials as htm


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
        assert isinstance(prop.pre_exp, (float, int))
        assert isinstance(prop.act_energy, (float, int))
        assert prop.isotope


def test_all_properties_have_references():
    for prop in htm.database:
        assert prop.author
        assert prop.year
        assert prop.source
