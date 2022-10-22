import h_transport_materials as htm


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
