import h_transport_materials as htm

import matplotlib.pyplot as plt

fig = htm.plotting.plot_plotly(
    htm.diffusivities.filter(material=[htm.PALLADIUM, htm.VANADIUM, htm.TUNGSTEN]),
    colour_by="material",
    show_datapoints=False,
)

fig.write_html("out.html")
