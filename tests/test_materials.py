import pytest
import h_transport_materials as htm


@pytest.mark.parametrize(
    "material,group",
    [
        (mat, group)
        for mat in ["tungsten", "copper", "cucrzr", "flinak", "lipb"]
        for group in [htm.diffusivities, htm.solubilities]
    ],
)
def test_units_wrong_value(material, group):
    """Checks that material is found in the group

    Args:
        material (str): the searched material
        group (htm.PropertyGroup): the group of properties
    """
    filtered_group = group.filter(material=material)

    assert len(filtered_group.properties) > 0
