import h_transport_materials as htm
import h_transport_materials.conversion as c
import numpy as np


def test_J_per_mol_to_eV_regression():
    """regression test for J_per_mol to eV"""
    value = 20  # J
    assert value == c.eV_to_J_per_mol(c.J_per_mol_to_eV(value))


def test_J_per_mol_to_eV():
    value = 11
    assert c.J_per_mol_to_eV(value) == 11 * htm.k_B / htm.Rg


def test_kcal_to_J():
    value = 12
    assert c.kcal_to_J(value) == 4184 * value


def test_kcal_to_J_regression():
    value = 30
    assert c.kcal_to_J(c.J_to_kcal(value)) == value


def test_kJ_per_mol_to_eV():
    value = 13
    assert c.kJ_per_mol_to_eV(value) == c.J_per_mol_to_eV(value * 1000)


def test_kcal_per_mol_to_eV():
    value = 22
    assert c.kcal_per_mol_to_eV(value) == c.J_per_mol_to_eV(c.kcal_to_J(value))


def test_atm_to_Pa():
    value = 62

    assert c.atm_to_Pa(value) == 101325 * value


def test_atm_to_Pa_reg():
    value = 56

    assert np.isclose(c.atm_to_Pa(c.Pa_to_atm(value)), value)


def test_bar_to_Pa():
    value = 16

    assert c.bar_to_Pa(value) == value * 1e5


def test_bar_to_Pa_reg():
    value = 12.5

    assert c.bar_to_Pa(c.Pa_to_bar(value)) == value


def test_Torr_to_Pa():
    value = 12.6

    assert np.isclose(c.Torr_to_Pa(value), value * 133.322)


def test_Torr_to_Pa_reg():

    value = 13.5

    assert np.isclose(c.Torr_to_Pa(c.Pa_to_Torr(value)), value)


def test_cmHg_conversion():
    value = 12

    assert c.cmHg_to_Pa(value) == 1333.22 * value


def test_ccSTP_to_mol():
    P = 101.35e3  # Pa
    T = 273.15  # K
    R = htm.Rg

    V_cm3 = 1.5  # cm3
    V_m3 = V_cm3 * 1e-6  # m3

    expected_n = P * V_m3 / (R * T)
    print(expected_n)

    assert expected_n == c.ccSTP_to_mol(V_cm3)
