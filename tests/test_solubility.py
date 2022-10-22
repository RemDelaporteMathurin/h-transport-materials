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


def test_pre_exp_can_be_quantity():
    htm.Solubility(
        units="m-3 Pa-1/2",
        S_0=1 * htm.ureg.particle * htm.ureg.meter**-3 * htm.ureg.bar**-0.5,
        E_S=0.5,
    )


def test_act_energy_can_be_quantity():
    htm.Solubility(
        units="m-3 Pa-1/2",
        S_0=1,
        E_S=0.5*htm.ureg.kJ * htm.ureg.mol**-1,
    )
