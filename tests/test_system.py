import h_transport_materials as htm

ALL_PROPS = htm.diffusivities.properties + htm.solubilities.properties


def test_all_solubilities_are_solubility():
    for sol in htm.solubilities:
        assert isinstance(sol, htm.Solubility)


def test_all_diffusivities_are_diffusivity():
    for diff in htm.diffusivities:
        assert isinstance(diff, htm.Diffusivity)


def test_all_properties_have_required_attributes():
    for prop in ALL_PROPS:
        assert prop.material
        assert isinstance(prop.pre_exp, (float, int))
        assert isinstance(prop.act_energy, (float, int))


def test_all_properties_have_references():
    for prop in ALL_PROPS:
        assert prop.author
        assert prop.year
        assert prop.source
