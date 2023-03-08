import pytest

import h_transport_materials as htm


def test_permeability_henry():
    """Tests that a Henry permeability can be set"""
    prop = htm.Permeability(
        pre_exp=1
        * htm.ureg.particle
        * htm.ureg.meter**-1
        * htm.ureg.second**-1
        * htm.ureg.Pa**-1,
        act_energy=1 * htm.ureg.eV * htm.ureg.particle**-1,
    )
    assert prop.law == "henry"


def test_permeability_sievert():
    """Tests that a Sievert permeability can be set"""
    prop = htm.Permeability(
        pre_exp=1
        * htm.ureg.particle
        * htm.ureg.meter**-1
        * htm.ureg.second**-1
        * htm.ureg.Pa**-0.5,
        act_energy=1 * htm.ureg.eV * htm.ureg.particle**-1,
    )
    assert prop.law == "sievert"


def test_users_have_to_give_units_pre_exp():
    with pytest.raises(ValueError, match="units are required for Permeability"):
        htm.Permeability(
            pre_exp=1, act_energy=0.1 * htm.ureg.eV * htm.ureg.particle**-1
        )


def test_users_have_to_give_units_data_y():
    with pytest.raises(ValueError, match="units are required for Permeability"):
        htm.Permeability(data_y=[1, 2], data_T=[1, 2] * htm.ureg.K)


@pytest.mark.filterwarnings("ignore:no units were given")
def test_without_units_but_law():
    prop = htm.Permeability(1, 0, law="sievert")
    assert prop.pre_exp.units == prop.units
