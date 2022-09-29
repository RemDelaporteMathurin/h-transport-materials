import h_transport_materials as htm


def kJ_per_mol_to_eV(E):
    E_in_J = E * 1000
    return J_per_mol_to_eV(E_in_J)


def J_per_mol_to_eV(E):
    return E * htm.k_B / htm.Rg  # eV


def eV_to_J_per_mol(E):
    return E * htm.Rg / htm.k_B


def kcal_to_J(E):
    return 4184 * E


def J_to_kcal(E):
    return E / 4184


def kcal_per_mol_to_eV(E):
    E_in_J = kcal_to_J(E)
    return J_per_mol_to_eV(E_in_J)
