import inspect


class Material:
    """Base Material class

    Args:
        name (str): the name of the material
    """

    family = "material"

    def __init__(self, name: str):
        self.name = name

    @property
    def parents(self):
        return [_ for _ in self.__class__.__mro__ if _ not in [object]]

    def __eq__(self, mat) -> bool:
        if isinstance(mat, str):
            matching_name = self.name == mat
            matching_family = mat in [p.family for p in self.parents]
            return matching_name or matching_family
        elif inspect.isclass(mat):
            return isinstance(self, mat)
        else:
            return super.__eq__(self, mat)

    def __str__(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self.name)


class PlasmaFacing(Material):
    family = "plasma facing"


class Metal(Material):
    family = "metal"


class Alloy(Metal):
    family = "alloy"


class Compound(Metal):
    family = "compound"


class PureMetal(Metal):
    """Pure metal

    Args:
        name (str): the name of the material
        symbol (str, optional): the element symbol. Defaults to None.
    """

    family = "pure metal"

    def __init__(self, name: str, symbol: str = None):
        super().__init__(name)
        self.symbol = symbol

    def __eq__(self, mat) -> bool:
        if isinstance(mat, str):
            if self.symbol == mat:
                return True

        return super().__eq__(mat)

    def __hash__(self):
        return hash(self.name)


class Hastelloy(Alloy):
    family = "hastelloy"


class Steel(Alloy):
    family = "steel"


class Inconel(Alloy):
    family = "inconel"


class TungstenAlloy(Alloy, PlasmaFacing):
    family = "tungsten alloy"


class Tungsten(PureMetal, PlasmaFacing):
    def __init__(self):
        super().__init__("tungsten", symbol="W")


class Beryllium(PureMetal, PlasmaFacing):
    def __init__(self):
        super().__init__("beryllium", symbol="Be")


class Carbon(PureMetal, PlasmaFacing):
    def __init__(self):
        super().__init__("carbon", symbol="C")


class MoltenSalt(Material):
    family = "molten salt"


TUNGSTEN = Tungsten()
BERYLLIUM = Beryllium()
CARBON = Carbon()
GOLD = PureMetal("gold", "Au")
HASTELLOY_X = Hastelloy("hastelloy_x")
HASTELLOY_N = Hastelloy("hastelloy_n")
STEEL_316L = Steel("316l_steel")
INCOLOY_800 = Alloy("incoloy_800")
INCONEL_600 = Inconel("inconel_600")
INCONEL_625 = Inconel("inconel_625")
INCONEL_750 = Inconel("inconel_750")
IRON = PureMetal("iron", "Fe")
MOLYBDENUM = PureMetal("molybdenum", "Mo")
NICKEL = PureMetal("nickel", "Ni")
NIMONIC_80A = Alloy("nimonic_80a")
NIOBIUM = PureMetal("niobium", "Nb")
PALLADIUM = PureMetal("palladium", "Pd")
STEEL_RAFM = Steel("rafm_steel")
STEEL_SERIES_300 = Steel("series_300_steel")
SILVER = PureMetal("silver", "Ag")
STEEL_304 = Steel("304_steel")
TANTALUM = PureMetal("tantalum", "Ta")
TITANIUM = PureMetal("titanium", "Ti")
V4CR4TI = Alloy("v4cr4ti")
VANADIUM = PureMetal("vanadium", "V")
ALUMINIUM = PureMetal("aluminium", "Al")
COPPER = PureMetal("copper", "Cu")
CUCRZR = Alloy("cucrzr")
FLIBE = MoltenSalt("flibe")
FLINAK = MoltenSalt("flinak")
LIPB = Alloy("lipb")
LITHIUM = PureMetal("lithium", "Li")
PDAG = Alloy("pdag")
ZIRCONIUM = PureMetal("zirconium", "Zr")

ALUMINA = Compound("alumina")
