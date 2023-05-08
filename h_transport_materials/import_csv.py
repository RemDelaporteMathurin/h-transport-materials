from pathlib import Path
import numpy as np


def import_csv(filename: str, current_file, **kwargs):
    """_summary_

    Args:
        filename (str): _description_
        current_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = np.genfromtxt(str(Path(current_file).parent) + "/" + filename, **kwargs)
    return data


def structure_data_from_wpd(data: np.ndarray):
    """Returns a structured dataset based on a numpy array from WebPlotDigitizer

    Args:
        data (np.ndarray): the data imported with np.genfromtxt(..., names=True)

    Returns:
        dict: structured dictionary with keys corresponding to field names.
            Ex: {"fieldA": {"x": [1,2,3], "y": [1,2,3]}}
    """
    if not data.dtype.names:
        raise ValueError("data.dtype.names should not be None.")
    structured_data = {}
    names = data.dtype.names
    for name_x, name_y in zip(names[0::2], names[1::2]):
        x = data[name_x]
        y = data[name_y]
        structured_data[name_x] = {"x": x, "y": y}
    return structured_data
