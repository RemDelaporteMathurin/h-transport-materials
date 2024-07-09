import json
from datetime import datetime
import matplotlib.pyplot as plt
from packaging import version


def annotate_version_tags(tags, dates, y, offset=0):
    for tag, date, y_val in zip(tags, dates, y):
        if version.parse(tag).micro == 0:
            plt.annotate(tag, (date, y_val + offset), color="tab:grey")


with open("releases.json") as f:
    releases_dict = json.load(f)

tags = []
dates = []
nb_props, nb_diffs, nb_sols, nb_perms, nb_recombs, nb_diss = [], [], [], [], [], []
nb_mats = []
nb_refs = []
for tag, data in releases_dict.items():
    datetime_object = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
    dates.append(datetime_object)
    tags.append(tag)
    if "nb_props" in data:
        nb_props.append(data["nb_props"])
    else:
        nb_props.append(0)
    if "nb_diffs" in data:
        nb_diffs.append(data["nb_diffs"])
    else:
        nb_diffs.append(0)
    if "nb_sols" in data:
        nb_sols.append(data["nb_sols"])
    else:
        nb_sols.append(0)
    if "nb_perm" in data:
        nb_perms.append(data["nb_perm"])
    else:
        nb_perms.append(0)
    if "nb_recomb" in data:
        nb_recombs.append(data["nb_recomb"])
    else:
        nb_recombs.append(0)
    if "nb_diss" in data:
        nb_diss.append(data["nb_diss"])
    else:
        nb_diss.append(0)
    if "nb_mats" in data:
        nb_mats.append(data["nb_mats"])
    else:
        nb_mats.append(0)
    if "nb_refs" in data:
        nb_refs.append(data["nb_refs"])
    else:
        nb_refs.append(0)

tags = [x for _, x in sorted(zip(dates, tags))]
nb_props = [x for _, x in sorted(zip(dates, nb_props))]
nb_diffs = [x for _, x in sorted(zip(dates, nb_diffs))]
nb_sols = [x for _, x in sorted(zip(dates, nb_sols))]
nb_perms = [x for _, x in sorted(zip(dates, nb_perms))]
nb_recombs = [x for _, x in sorted(zip(dates, nb_recombs))]
nb_diss = [x for _, x in sorted(zip(dates, nb_diss))]
nb_mats = [x for _, x in sorted(zip(dates, nb_mats))]
nb_refs = [x for _, x in sorted(zip(dates, nb_refs))]
dates = sorted(dates)

fig, (ax_mats, ax_refs, ax_props) = plt.subplots(
    nrows=3, ncols=1, sharex=True, figsize=(11, 8)
)
plt.suptitle("The evolution of the HTM database", weight="bold")

plt.sca(ax_props)
plt.plot(dates, nb_props)
plt.scatter(
    [date for tag, date in zip(tags, dates) if version.parse(tag).micro == 0],
    [nb_prop for tag, nb_prop in zip(tags, nb_props) if version.parse(tag).micro == 0],
    zorder=3,
    color="tab:blue",
)


plt.stackplot(
    dates,
    nb_diffs,
    nb_sols,
    nb_perms,
    nb_recombs,
    nb_diss,
    alpha=0.5,
    labels=[
        "diffusivities",
        "solubilities",
        "permeabilities",
        "recomb. coeffs",
        "diss. coeffs",
    ],
)

annotate_version_tags(tags, dates, nb_props, offset=5)
plt.ylabel("Properties", rotation=0, ha="right", weight="bold")
plt.legend()
handles, labels = plt.gca().get_legend_handles_labels()
plt.gca().legend(handles[::-1], labels[::-1])

plt.sca(ax_mats)
plt.ylabel("Materials", rotation=0, ha="right", weight="bold")
plt.fill_between(dates, nb_mats, alpha=0.2)
plt.scatter(
    [date for tag, date in zip(tags, dates) if version.parse(tag).micro == 0],
    [nb_mat for tag, nb_mat in zip(tags, nb_mats) if version.parse(tag).micro == 0],
    zorder=3,
    color="tab:blue",
)
annotate_version_tags(tags, dates, nb_mats, offset=2)
plt.plot(dates, nb_mats)
plt.ylim(bottom=0)

plt.sca(ax_refs)
plt.ylabel("References", rotation=0, ha="right", weight="bold")
plt.fill_between(dates, nb_refs, alpha=0.2)
plt.scatter(
    [date for tag, date in zip(tags, dates) if version.parse(tag).micro == 0],
    [nb_ref for tag, nb_ref in zip(tags, nb_refs) if version.parse(tag).micro == 0],
    zorder=3,
    color="tab:blue",
)
annotate_version_tags(tags, dates, nb_refs, offset=2)
plt.plot(dates, nb_refs)
plt.ylim(bottom=0)

for ax in (ax_refs, ax_mats, ax_props):
    ax.spines[["right", "top"]].set_visible(False)
    ax.yaxis.grid(alpha=0.3)

plt.tight_layout()

plt.savefig("evolution.png", dpi=300)
plt.show()
