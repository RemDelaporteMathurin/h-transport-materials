class Material:
    family = None

    def __init__(self, name: str):
        self.name = name

    @property
    def parents(self):
        return [_ for _ in self.__class__.__mro__ if _ not in [object, Material]]

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            match_name = self.name == __o
            match_family = any([parent.family == __o for parent in self.parents])
            return match_name or match_family
        else:
            return super().__eq__(__o)


class PlasmaFacing(Material):
    family = "plasma facing"


class Metal(Material):
    family = "metal"


class Alloy(Metal):
    family = "alloy"


class PureMetal(Metal):
    family = "pure metal"

    def __init__(self, name: str, symbol: str = None):
        super().__init__(name)
        self.symbol = symbol

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            if self.symbol == __o:
                return True

        return super().__eq__(__o)


class Steel(Alloy):
    family = "steel"


class Inconel(Alloy):
    family = "inconel"


class TungstenAlloy(Alloy, PlasmaFacing):
    family = "tungsten alloy"


class Tungsten(PureMetal, PlasmaFacing):
    family = "tungsten"

    def __init__(self):
        super().__init__("tungsten", symbol="W")


class Beryllium(PureMetal, PlasmaFacing):
    family = "beryllium"

    def __init__(self):
        super().__init__("beryllium", symbol="Be")


tungsten = Tungsten()
beryllium = Beryllium()
