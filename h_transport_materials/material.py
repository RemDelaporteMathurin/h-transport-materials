class Material:
    family = None

    def __init__(self, name: str):
        self.name = name

    @property
    def parents(self):
        return [_ for _ in self.__class__.__mro__ if _ not in [object, Material]]


class PlasmaFacing(Material):
    family = "plasma facing"


class Metal(Material):
    family = "metal"


class Alloy(Metal):
    family = "alloys"


class PureMetal(Metal):
    family = "pure metals"

    def __init__(self, name: str, symbol: str = None):
        super().__init__(name)
        self.symbol = symbol


class Steel(Alloy):
    family = "steel"


class Inconel(Alloy):
    family = "Inconel"


class TungstenAlloys(Alloy, PlasmaFacing):
    family = "tungsten alloys"


class Tungsten(PureMetal, PlasmaFacing):
    family = "tungsten"

    def __init__(self):
        super().__init__("tungsten", symbol="W")


tungsten = Tungsten()
