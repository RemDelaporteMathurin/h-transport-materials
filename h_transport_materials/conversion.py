import h_transport_materials as htm


STP = (273.15 * htm.ureg.K, 1 * htm.ureg.bar)
NTP = (293.15 * htm.ureg.K, 1 * htm.ureg.atm)


def volume_STP_to_mol(V):
    T, P = STP
    return (P * V / (htm.Rg * T)).to(htm.ureg.mol)


def volume_NTP_to_mol(V):
    T, P = NTP
    return (P * V / (htm.Rg * T)).to(htm.ureg.mol)


htm.ureg.define(f"cubiccentimeterNTP = {volume_NTP_to_mol(1 * htm.ureg.cm**3)} = ccNTP")
htm.ureg.define(f"cubiccentimeterSTP = {volume_STP_to_mol(1 * htm.ureg.cm**3)} = ccSTP")
htm.ureg.define(f"atomfraction = 1 * particle / particle = atfr")

assert "ccNTP" in htm.ureg
assert "ccSTP" in htm.ureg
assert "atfr" in htm.ureg
