# H-transport-materials
![CI](https://github.com/RemDelaporteMathurin/h_transport_materials/actions/workflows/ci.yml/badge.svg)

## Installation

```
pip install h-transport-materials
```

## Usage
### Access the internal database:
```python
import h_transport_materials as htm
import matplotlib.pyplot as plt

# filter only tungsten and H
diffusivities = htm.diffusivities.filter(material="tungsten").filter(isotope="h")

for D in diffusivities:
    htm.plotting.plot(D)


plt.yscale("log")
plt.ylabel("Diffusivity (m$^2$/s)")
plt.legend()
plt.show()
```
![Figure_1](https://user-images.githubusercontent.com/40028739/169280320-c4d45d9b-7f33-4628-a4fd-72e81be16124.svg)

### Add custom properties

```python
import h_transport_materials as htm

import numpy as np

# Create a custom property
my_custom_property = htm.ArheniusProperty(pre_exp=1e-5, act_energy=0.2)

# From (T, y) data
my_fitted_property = htm.ArheniusProperty(
    data_T=np.array([300, 400, 500, 600]), data_y=np.array([1e-8, 1e-7, 1e-6, 1e-5])
)

print("Pre-exponential factor: {:.2e}".format(my_fitted_property.pre_exp))
print("Activation energy: {:.2f} eV".format(my_fitted_property.act_energy))

# Pre-exponential factor: 4.40e-03
# Activation energy: 0.35 eV
```

### Filters

```python
import h_transport_materials as htm

# tungsten solubilities
htm.solubilities.filter(material="tungsten")

# copper and cucrzr solubilities
htm.solubilities.filter(material=["copper", "cucrzr"])

# all_authors_except_ryabchikov
htm.diffusivities.filter(material="tungsten").filter(author="ryabchikov", exclude=True)

# only Tritium
htm.diffusivities.filter(isotope="t")
```

# Contributions

The current database is far from complete.
Contributions are most welcome to extend it by adding new properties and also new materials!
