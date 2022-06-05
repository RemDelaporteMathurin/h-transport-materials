import h_transport_materials as htm

# source_bib = """@article{article-minimal,
#     author = "L[eslie] B. Lamport",
#     title = "The Gnats and Gnus Document Preparation System",
#     journal = "G-Animal's Journal",
#     year = "1986"
# }
# """

# my_prop = htm.Property(material="my_mat", source=source_bib)
# my_prop3 = htm.Property(material="my_mat", source="source")

# my_group = htm.PropertiesGroup()
# my_group.properties = [my_prop, my_prop3]

# my_group.export_bib("out.bib")
# print(my_group.bibdata.to_string(bib_format="bibtex"))

tungsten = htm.solubilities.filter(material="tungsten")
tungsten.export_bib("out.bib")