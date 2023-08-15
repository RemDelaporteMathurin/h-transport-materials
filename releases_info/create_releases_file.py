import requests
from datetime import datetime
import json


def create_json_file():
    releases_dict = {}

    res = requests.get("https://pypi.org/pypi/h-transport-materials/json")
    d = res.json()
    for release_tag in d["releases"]:
        release_time = d["releases"][release_tag][0]["upload_time"]

        datetime_object = datetime.strptime(release_time, "%Y-%m-%dT%H:%M:%S")
        releases_dict[release_tag] = {"date": str(datetime_object)}

    with open("releases.json", "w") as f:
        json.dump(releases_dict, f, indent=4)


if __name__ == "__main__":
    print("creating file")
    create_json_file()
    print("file created")
