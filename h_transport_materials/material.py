import inspect


class Material:
    family = "material"

    def __init__(self, name: str):
        self.name = name

    @property
    def parents(self):
        return [_ for _ in self.__class__.__mro__ if _ not in [object, self.__class__]]

    def __eq__(self, mat) -> bool:
        if isinstance(mat, str):
            matching_name = self.name == mat
            matching_family = mat in [p.family for p in self.parents]
            return matching_name or matching_family
        elif inspect.isclass(mat):
            return isinstance(self, mat)
        else:
            return super.__eq__(self, mat)


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

    def __eq__(self, mat) -> bool:
        if isinstance(mat, str):
            if self.symbol == mat:
                return True

        return super().__eq__(mat)


class Steel(Alloy):
    family = "steel"


class Steel316L(Steel):
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


TUNGSTEN = Tungsten()
BERYLLIUM = Beryllium()
