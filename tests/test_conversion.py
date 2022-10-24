import h_transport_materials as htm
import h_transport_materials.conversion as c


def test_ccSTP_to_mol():
    P = 101.35e3  # Pa
    T = 273.15  # K
    R = htm.Rg

    V_cm3 = 1.5  # cm3
    V_m3 = V_cm3 * 1e-6  # m3

    expected_n = P * V_m3 / (R * T)
    print(expected_n)

    assert expected_n == c.ccSTP_to_mol(V_cm3)
