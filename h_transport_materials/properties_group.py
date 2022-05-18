import json
from pathlib import Path

from h_transport_materials.property import ArheniusProperty


class PropertiesGroup:
    def __init__(self) -> None:
        self.data = {}
        self.properties = []

    def __getitem__(self, item):
        return self.properties[item]

    def filter(self, **kwargs):
        """_summary_

        Returns:
            PropertiesGroup or htm.Property: _description_
        """
        list_of_props = PropertiesGroup()
        list_of_searched_props = self.properties
        for key, value in kwargs.items():
            for prop in list_of_searched_props:
                if getattr(prop, key) == value:
                    list_of_props.properties.append(prop)
        return list_of_props

    def add_properties_from_dir(self, directory, verbose: bool = True, recursive=True):
        if verbose is True:
            print("searching directory", directory)
        if recursive:
            filelist = Path(directory).rglob("*.json")
        else:
            filelist = Path(directory).glob("*.json")
        for filename in filelist:
            if verbose is True:
                print(f"loading {filename}")
            self.add_properties_from_file(filename, verbose)

    def add_properties_from_file(self, filename: str, verbose: bool = True):
        """Add materials to the internal library from a json file"""
        if verbose:
            print(f"Added materials to library from {filename}")
        with open(filename, "r") as f:
            new_data = json.load(f)
            if verbose:
                print("Added material", list(new_data.keys()))
            self.data.update(new_data)

    def make_properties_from_data(self):
        for prop_name, kwargs in self.data.items():
            self.properties.append(ArheniusProperty(**kwargs))


diffusivities = PropertiesGroup()
diffusivities.add_properties_from_dir(
    Path(__file__).parent / "data/diffusivities", verbose=False
)
diffusivities.make_properties_from_data()

solubilities = PropertiesGroup()
solubilities.add_properties_from_dir(
    Path(__file__).parent / "data/solubilities", verbose=False
)
solubilities.make_properties_from_data()
