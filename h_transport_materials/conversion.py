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


# PRESSURE

atm_to_Pa_factor = 101325  # Pa/atm


def atm_to_Pa(P):
    return atmn_to_Pan(P, n=1)


def Pa_to_atm(P):
    return Pan_to_atmn(P, n=1)


def atmn_to_Pan(P, n):
    """Converts values in atm^n to Pa^n

    Args:
        P (float): the sqrt pressure in atm^n

    Returns:
        float: the sqrt pressure in atm^n
    """
    return P * atm_to_Pa_factor**n


def Pan_to_atmn(P, n):
    return P / (atm_to_Pa_factor**n)


def bar_to_Pa(P):
    return P * 1e5


def Pa_to_bar(P):
    return P * 1e-5


def Torr_to_Pa(P):
    return P * 133.322


def Pa_to_Torr(P):
    return P / 133.322


def cmHg_to_Pa(P):
    return 1333.22 * P


def cmHgn_to_Pan(P, n):
    return 1333.22**n * P


def ccSTP_to_mol(V):
    """Converts a volume in cc (STP) (aka cubic centimetre) to mol
    assuming a perfect gas law PV = nRT

    Args:
        V (float): The volume in cc STP

    Returns:
        float: the number of moles (mol)
    """
    # STP pressure, temperature
    P = 101.35e3  # Pa
    T = 273.15  # K

    R = htm.Rg

    V_m3 = V * 1e-6  # m3

    n = P * V_m3 / (R * T)  # mol

    return n
