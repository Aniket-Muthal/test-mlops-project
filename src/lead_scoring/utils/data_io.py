"""
data_io.py
----------

Lightweight utilities for pipeline I/O operations.

Functions:
- load_yaml(): Read a YAML file and return its contents.
- create_directories(): Safely create one or more directories if they do not already exist.
"""


## ---------------------------------------------------------------------------------------- ##
import yaml
from typing import List
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError


## ---------------------------------------------------------------------------------------- ##
def load_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Load a YAML file and return its contents as a ConfigBox.

    Parameters
    ----------
    path_to_yaml : Path
        Path to the YAML file

    Returns
    -------
    ConfigBox
        Parsed YAML content with attribute-style access

    Raises
    ------
    ValueError : If the YAML file is empty or invalid
    Exception : For other unexpected errors
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise ValueError(f"YAML file at {path_to_yaml} is empty")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is invalid or contains unsupported values")
    except Exception as e:
        raise e

## ---------------------------------------------------------------------------------------- ##  
def create_directories(list_dir_path: List[str]):
    """
    Create directories

    Parameters
    ----------
    list_dir_path : List[str]
        A list of directory paths (as strings) to be created

    Notes
    -----
    - Uses `parents=True` to create intermediate directories if needed
    - Uses `exist_ok=True` to prevent errors when directories already exist
    """
    for dir_path in list_dir_path:
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)


## ---------------------------------------------------------------------------------------- ##