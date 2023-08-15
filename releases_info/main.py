import sys
import subprocess
import json

subprocess.run([sys.executable, "./create_releases_file.py"])

with open("releases.json") as f:
    releases_dict = json.load(f)

for version_tag in releases_dict:
    print(f"installing version {version_tag}")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            f"h-transport-materials=={version_tag}",
        ]
    )
    subprocess.run(
        [sys.executable, "./compute_version_info.py", f"--version={version_tag}"]
    )
