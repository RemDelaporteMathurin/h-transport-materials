import h_transport_materials as htm


def test_permeability_henry():
    """Tests that a Henry permeability can be set"""
    htm.Permeability(
        pre_exp=1
        * htm.ureg.particle
        * htm.ureg.meter**-1
        * htm.ureg.second**-1
        * htm.ureg.Pa**-1,
        act_energy=1 * htm.ureg.eV * htm.ureg.particle**-1,
        law="henry",
    )
