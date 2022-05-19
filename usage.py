import h_transport_materials as htm
import matplotlib.pyplot as plt

#
tungsten_diffusivities = htm.diffusivities.filter(material="tungsten")

# compute mean diffusivity
mean_D_0, mean_E_D = tungsten_diffusivities.mean()
D_mean = htm.ArheniusProperty(mean_D_0, mean_E_D)

# plot
for D in tungsten_diffusivities:
    htm.plotting.plot(D, alpha=0.5)

htm.plotting.plot(D_mean, color="black", linewidth=3)


# annotate
x_annotation = 0.0034
plt.annotate("mean value", (x_annotation, D_mean.value(T=1 / x_annotation)))

plt.ylabel("Diffusivity (m$^2$ s$^{-1}$)")
plt.yscale("log")
plt.show()
