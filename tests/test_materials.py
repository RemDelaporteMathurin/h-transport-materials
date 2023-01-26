import pytest
import h_transport_materials as htm


@pytest.mark.parametrize(
    "material",
    ["tungsten", "copper", "cucrzr", "flinak", "lipb", "flibe"],
)
def test_units_wrong_value(material):
    """Checks that material is found in the group

    Args:
        material (str): the searched material
    """
    filtered_group = htm.database.filter(material=material)

    assert len(filtered_group) > 0


def test_print():
    print(htm.ALUMINIUM)
