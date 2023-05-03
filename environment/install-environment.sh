set -e

# Get and install mambaforge
if [ ! -d "$HOME/mambaforge" ]; then
  curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-$(uname)-$(uname -m).sh
  bash Mambaforge-$(uname)-$(uname -m).sh -b -p "$HOME/mambaforge"
  rm Mambaforge-$(uname)-$(uname -m).sh
fi

# Create the environment
mamba env create -f environment/environment.yml
mamba activate htm
