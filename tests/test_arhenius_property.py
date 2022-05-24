import pytest
import numpy as np

import h_transport_materials as htm


@pytest.mark.parametrize(
    "data_T,data_y",
    [
        (
            T_0 + delta_T * np.random.random_sample(size=10),
            y_0 + delta_y * np.random.random_sample(size=10),
        )
        for T_0 in [300, 600]
        for delta_T in [100, 1]
        for y_0 in [500, 1000]
        for delta_y in [100, 1]
    ],
)
def test_fit(data_T, data_y):
    expected_values = htm.fitting.fit_arhenius(data_y, data_T)

    my_prop = htm.ArrheniusProperty(data_T=data_T, data_y=data_y)

    my_prop.fit()
    computed_values = my_prop.pre_exp, my_prop.act_energy
    assert expected_values == computed_values


def test_pre_exp_getter_fit():
    my_prop = htm.ArrheniusProperty(
        data_T=300 + 100 * np.random.random_sample(size=10),
        data_y=100 + 600 * np.random.random_sample(size=10),
    )

    computed_pre_exp = my_prop.pre_exp

    my_prop.fit()
    expected_pre_exp = my_prop.pre_exp

    assert computed_pre_exp == expected_pre_exp


def test_act_energy_getter_fit():
    my_prop = htm.ArrheniusProperty(
        data_T=300 + 100 * np.random.random_sample(size=10),
        data_y=100 + 600 * np.random.random_sample(size=10),
    )

    computed_act_energy = my_prop.act_energy

    my_prop.fit()
    expected_act_energy = my_prop.act_energy

    assert computed_act_energy == expected_act_energy


@pytest.mark.parametrize(
    "T,pre_exp,act_energy", [(300, 3, 0.2), (205, 6, 0.8), (600, 1e5, 1.2)]
)
def test_value(T, pre_exp, act_energy):
    my_prop = htm.ArrheniusProperty(pre_exp=pre_exp, act_energy=act_energy)

    computed_value = my_prop.value(T=T)
    expected_value = pre_exp * np.exp(-act_energy / htm.k_B / T)
    assert expected_value == computed_value


def test_fit_creates_temp_range():
    """Checks that when given data_T and data_y,
    ArrheniusProperty.range is based on data_T"""
    my_prop = htm.ArrheniusProperty(
        data_T=[300, 400, 500],
        data_y=[1, 2, 3],
    )

    assert my_prop.range == (300, 500)
