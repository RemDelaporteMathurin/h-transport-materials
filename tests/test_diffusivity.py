import h_transport_materials as htm


def test_pre_exp_can_be_quantity():
    prop = htm.Diffusivity(
        D_0=1 * htm.ureg.cm**2 * htm.ureg.second**-1,
        E_D=0.5,
    )

    assert prop.pre_exp == 1e-4


def test_act_energy_can_be_quantity():
    prop = htm.Diffusivity(
        D_0=1,
        E_D=0.5 * htm.ureg.kJ * htm.ureg.mol**-1,
    )
    assert prop.act_energy != 0.5
