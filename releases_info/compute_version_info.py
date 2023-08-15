import json
import h_transport_materials as htm
import numpy as np
import packaging.version
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--version", type=str, required=True)
args = parser.parse_args()


def len_group(group, version_tag):
    if packaging.version.parse(version_tag) < packaging.version.parse("0.6"):
        return len(group.properties)
    else:
        return len(group)


def all_props(version_tag):
    if packaging.version.parse(version_tag) >= packaging.version.parse("0.6"):
        return htm.database
    else:
        return htm.diffusivities.properties + htm.solubilities.properties


def compute_information(version_tag):

    with open("releases.json") as f:
        releases_dict = json.load(f)

    releases_dict[version_tag]["nb_diffs"] = len_group(htm.diffusivities, version_tag)
    releases_dict[version_tag]["nb_sols"] = len_group(htm.solubilities, version_tag)
    releases_dict[version_tag]["nb_props"] = len_group(
        htm.diffusivities, version_tag
    ) + len_group(htm.solubilities, version_tag)

    if packaging.version.parse(version_tag) >= packaging.version.parse("0.6"):
        releases_dict[version_tag]["nb_props"] = len_group(htm.database, version_tag)
        releases_dict[version_tag]["nb_perm"] = len_group(
            htm.permeabilities, version_tag
        )
        releases_dict[version_tag]["nb_recomb"] = len_group(
            htm.recombination_coeffs, version_tag
        )
        releases_dict[version_tag]["nb_diss"] = len_group(
            htm.dissociation_coeffs, version_tag
        )

    if packaging.version.parse(version_tag) < packaging.version.parse("0.9"):
        releases_dict[version_tag]["nb_mats"] = len(
            np.unique([prop.material for prop in all_props(version_tag)])
        )
    else:
        releases_dict[version_tag]["nb_mats"] = len(
            np.unique([prop.material.name for prop in all_props(version_tag)])
        )

    releases_dict[version_tag]["nb_refs"] = len(
            np.unique([prop.source for prop in all_props(version_tag)])
        )

    with open("releases.json", "w") as f:
        json.dump(releases_dict, f, indent=4)


if __name__ == "__main__":
    print(f"adding version {args.version} to file")
    compute_information(args.version)
