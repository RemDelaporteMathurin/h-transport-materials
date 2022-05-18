class PropertiesGroup:
    def __init__(self) -> None:
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
