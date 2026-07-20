import os
import yaml


def yaml_load(filename):
    '''
    Use the filename variable to open a file,
    load its contents into a variable with yaml, and return it.
    '''
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    with open(filename, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data