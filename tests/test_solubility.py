import pytest

import h_transport_materials as htm


def test_users_have_to_give_units_pre_exp():
    with pytest.raises(ValueError, match="units are required for Solubility"):
        htm.Solubility(S_0=1, E_S=0.1 * htm.ureg.eV * htm.ureg.particle**-1)


def test_users_have_to_give_units_data_y():
    with pytest.raises(ValueError, match="units are required for Solubility"):
        htm.Solubility(data_y=[1, 2], data_T=[1, 2] * htm.ureg.K)


@pytest.mark.filterwarnings("ignore:no units were given")
def test_without_units_but_law():
    prop = htm.Solubility(1, 0, law="sievert")
    assert prop.pre_exp.units == prop.units
