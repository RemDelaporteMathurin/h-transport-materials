import pytest
import numpy as np

import h_transport_materials as htm


def test_fit():
    pass


def test_pre_exp_getter_fit():
    pass


def test_act_energy_getter_fit():
    pass


@pytest.mark.parametrize(
    "T,pre_exp,act_energy", [(300, 3, 0.2), (205, 6, 0.8), (600, 1e5, 1.2)]
)
def test_value(T, pre_exp, act_energy):
    my_prop = htm.ArheniusProperty(pre_exp=pre_exp, act_energy=act_energy)

    computed_value = my_prop.value(T=T)
    expected_value = pre_exp * np.exp(-act_energy / htm.k_B / T)
    assert expected_value == computed_value
