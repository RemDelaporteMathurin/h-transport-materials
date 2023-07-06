import pytest
import numpy as np

import h_transport_materials as htm
import pint


@pytest.mark.parametrize(
    "D_0,E_D",
    [
        (D_0, E_D)
        for D_0 in np.logspace(-7, 20, num=6) * htm.ureg.dimensionless
        for E_D in np.linspace(0.1, 1.5, num=5) * htm.ureg.eV * htm.ureg.particle**-1
    ],
)
def test_fit_arhenius(D_0, E_D):
    """Creates noisy data based on known D_0 and E_D coefficients.
    Fits the noisy data with an Arhenius law and compares the
    computed coefficients with the expected ones.
    """
    T = np.linspace(300, 1200) * htm.ureg.K
    D = D_0 * np.exp(-E_D / htm.k_B / T)

    # add noise
    noise = np.random.normal(0, 0.05, D.shape)
    noisy_D = D * 10**noise

    my_prop = htm.ArrheniusProperty(data_T=T, data_y=noisy_D)

    computed_D_0, computed_E_D = my_prop.pre_exp, my_prop.act_energy
    assert computed_D_0.magnitude == pytest.approx(D_0.magnitude, rel=0.3)
    assert computed_E_D.magnitude == pytest.approx(E_D.magnitude, rel=0.3)


def test_pre_exp_getter_fit():
    my_prop = htm.ArrheniusProperty(
        data_T=(300 + 100 * np.random.random_sample(size=10)) * htm.ureg.K,
        data_y=(100 + 600 * np.random.random_sample(size=10)) * htm.ureg.dimensionless,
    )

    computed_pre_exp = my_prop.pre_exp

    my_prop.fit()
    expected_pre_exp = my_prop.pre_exp

    assert computed_pre_exp == expected_pre_exp


def test_act_energy_getter_fit():
    my_prop = htm.ArrheniusProperty(
        data_T=(300 + 100 * np.random.random_sample(size=10)) * htm.ureg.K,
        data_y=(100 + 600 * np.random.random_sample(size=10)) * htm.ureg.dimensionless,
    )

    computed_act_energy = my_prop.act_energy

    my_prop.fit()
    expected_act_energy = my_prop.act_energy

    assert computed_act_energy == expected_act_energy


@pytest.mark.parametrize(
    "T,pre_exp,act_energy", [(300, 3, 0.2), (205, 6, 0.8), (600, 1e5, 1.2)]
)
def test_value(T, pre_exp, act_energy):
    pre_exp *= htm.ureg.dimensionless
    act_energy *= htm.ureg.eV * htm.ureg.particle**-1
    T *= htm.ureg.K
    my_prop = htm.ArrheniusProperty(pre_exp=pre_exp, act_energy=act_energy)

    computed_value = my_prop.value(T=T)
    expected_value = pre_exp * np.exp(-act_energy / htm.k_B / T)
    assert expected_value == computed_value


def test_fit_creates_temp_range():
    """Checks that when given data_T and data_y,
    ArrheniusProperty.range is based on data_T"""
    my_prop = htm.ArrheniusProperty(
        data_T=[300, 400, 500] * htm.ureg.K,
        data_y=[1, 2, 3] * htm.ureg.dimensionless,
    )

    assert my_prop.range == (300 * htm.ureg.K, 500 * htm.ureg.K)


@pytest.mark.parametrize("data", [[1, 2, 3, np.nan], np.array([1, 2, 3, np.nan])])
def test_data_T_removes_nan(data):
    """Checks that nan values are removed when assigned in data_T"""
    my_prop = htm.ArrheniusProperty(
        data_T=data * htm.ureg.K,
        data_y=data * htm.ureg.dimensionless,
    )
    assert np.count_nonzero(np.isnan(my_prop.data_T)) == 0


@pytest.mark.parametrize("data", [[1, 2, 3, np.nan], np.array([1, 2, 3, np.nan])])
def test_data_y_removes_nan(data):
    """Checks that nan values are removed when assigned in data_y"""
    my_prop = htm.ArrheniusProperty(
        data_T=data * htm.ureg.K,
        data_y=data * htm.ureg.dimensionless,
    )
    assert np.count_nonzero(np.isnan(my_prop.data_y)) == 0


def test_value_returns_pint_quantity():
    my_prop = htm.ArrheniusProperty(
        pre_exp=1 * htm.ureg.m**2 * htm.ureg.s**-1,
        act_energy=0.1 * htm.ureg.eV * htm.ureg.particle**-1,
    )

    T = htm.ureg.Quantity(400, htm.ureg.K)

    assert isinstance(my_prop.value(T), pint.Quantity)


def test_no_units_T_in_value_raises_warning():
    prop = htm.ArrheniusProperty(
        0.1 * htm.ureg.m**2 * htm.ureg.s**-1,
        act_energy=0.1 * htm.ureg.eV * htm.ureg.particle**-1,
    )
    with pytest.warns(UserWarning, match="no units were given with T"):
        prop.value(T=2)


def test_no_units_range_raises_warning():
    with pytest.warns(UserWarning, match="no units were given with temperature range"):
        htm.ArrheniusProperty(
            0.1 * htm.ureg.m**2 * htm.ureg.s**-1,
            act_energy=0.1 * htm.ureg.eV * htm.ureg.particle**-1,
            range=(100, 200),
        )


def test_no_units_data_T_raises_warning():
    with pytest.warns(UserWarning, match="no units were given with data_T"):
        htm.ArrheniusProperty(
            data_T=[100, 200],
            data_y=[
                100,
                200,
            ]
            * htm.ureg.m**2
            * htm.ureg.s**-1,
        )


def test_no_units_data_y_raises_warning():
    with pytest.warns(UserWarning, match="no units were given with data_y"):
        htm.ArrheniusProperty(
            data_T=[100, 200] * htm.ureg.K,
            data_y=[100, 200],
        )


def test_no_units_preexp_raises_warning():
    with pytest.warns(
        UserWarning, match="no units were given with pre-exponential factor"
    ):
        htm.ArrheniusProperty(
            0.1, act_energy=0.1 * htm.ureg.eV * htm.ureg.particle**-1
        )


def test_no_units_act_energy_raises_warning():
    with pytest.warns(UserWarning, match="no units were given with activation energy"):
        htm.ArrheniusProperty(0.1 * htm.ureg.m**2 * htm.ureg.s**-1, act_energy=0.1)


def test_multiply_properties():
    """Checks that two arrhenius props can be multiplied"""
    prop1 = htm.ArrheniusProperty(
        0.1 * htm.ureg.m**2 * htm.ureg.s**-1,
        act_energy=0.2 * htm.ureg.eV * htm.ureg.particle**-1,
    )
    prop2 = htm.ArrheniusProperty(
        0.5 * htm.ureg.m**2,
        act_energy=0.3 * htm.ureg.eV * htm.ureg.particle**-1,
    )

    product = prop1 * prop2

    assert isinstance(product, htm.ArrheniusProperty)
    assert product.pre_exp == prop1.pre_exp * prop2.pre_exp
    assert product.act_energy == prop1.act_energy + prop2.act_energy


@pytest.mark.parametrize("factor", [2, 1.0, 2.0, -3, -3.0])
def test_multiply_property_by_number(factor):
    """Checks that an arrhenius prop can be multiplied by a number"""
    prop1 = htm.ArrheniusProperty(
        0.1 * htm.ureg.m**2 * htm.ureg.s**-1,
        act_energy=0.2 * htm.ureg.eV * htm.ureg.particle**-1,
    )

    for product in [prop1 * factor, factor * prop1]:
        assert isinstance(product, htm.ArrheniusProperty)
        assert product.pre_exp == prop1.pre_exp * factor
        assert product.act_energy == prop1.act_energy


@pytest.mark.parametrize("factor", ["foo", [1, 2]])
def test_multiply_property_by_str(factor):
    """Checks that an arrhenius prop cannot be multiplied by non valid factors"""
    prop1 = htm.ArrheniusProperty(
        0.1 * htm.ureg.m**2 * htm.ureg.s**-1,
        act_energy=0.2 * htm.ureg.eV * htm.ureg.particle**-1,
    )

    error_msg = (
        "ArrheniusProperty can only be multiplied by ArrheniusProperty, int or float"
    )
    with pytest.raises(TypeError, match=error_msg):
        factor * prop1

    with pytest.raises(TypeError, match=error_msg):
        prop1 * factor
