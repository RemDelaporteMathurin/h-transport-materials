from pathlib import Path
import inspect
import numpy as np


def absolute_path(filename: str, level=1):
    """Returns the absolute path of a file. Based on a relative path.

    Args:
        filename (str): the relative path to the file
        level (int, optional): Level in the file call. 0 corresponds to
            the file where absolute_path is defined, 1 correspond to the
            file calling this function, 2 corresponds to the parent of
            the file calling this function. Defaults to 1.

    Returns:
        str: the absolute path of the file
    """
    caller_frame = inspect.stack()[level]
    return str(Path(caller_frame.filename).parent) + "/" + filename


def structure_data_from_wpd(filename: str):
    """Returns a structured dataset based on a csv file from WebPlotDigitizer
    exported with the "Export all data" option

    Args:
        filename (str): the relative path to the csv file

    Returns:
        dict: structured dictionary with keys corresponding to field names.
            Ex: {"fieldA": {"x": [1,2,3], "y": [1,2,3]}}
    """
    data = np.genfromtxt(
        absolute_path(filename, level=2),
        delimiter=",",
        names=True,
    )
    structured_data = {}
    names = data.dtype.names
    for name_x, name_y in zip(names[0::2], names[1::2]):
        x = data[name_x]
        y = data[name_y]
        structured_data[name_x] = {"x": x, "y": y}
    return structured_data
