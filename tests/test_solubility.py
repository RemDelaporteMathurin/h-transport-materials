import pytest

import h_transport_materials as htm


@pytest.mark.parametrize(
    "units",
    ["coucou", True, 0, 1, "mol m-3 Pa-1/2", "mol m-3 Pa-1"],
)
def test_units_wrong_value(units):
    with pytest.raises(
        ValueError, match="units can only accept m-3 Pa-1/2 or m-3 Pa-1"
    ):
        htm.Solubility(units=units)
