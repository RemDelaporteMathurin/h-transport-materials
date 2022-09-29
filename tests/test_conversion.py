import h_transport_materials as htm
import h_transport_materials.conversion as c


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
