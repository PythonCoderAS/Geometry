import inspect
import types
from typing import List, Union, Dict

import Geometry


def scan_module(mod: types.ModuleType) -> List[types.FunctionType]:
    """
    Scans the module provided using the inspect.getmembers function. It returns a list of functions.

    :param mod: The module to scan
    :type mod: types.ModuleType
    :return: The list of functions
    :rtype: list
    """

    funcs = []
    for item in inspect.getmembers(mod):
        if callable(item[1]):
            funcs.append(item[1])
    return funcs


def generate_directory(mod_dir: types.ModuleType) -> Dict[str, List[types.FunctionType]]:
    """
    Generates a dictionary where each entry is a module, and each entry contains a lit of functions retrieved from the
    `scan_module` function.

    :param mod_dir: The module package. Should be a module import that is a directory, such as Geometry.__init__
    :type mod_dir: types.ModuleType
    :return: The dictionary of items
    :rtype: dict
    """
    dictionary = {}
    for item in inspect.getmembers(mod_dir):
        if isinstance(item[1], types.ModuleType):
            dictionary[item[0]] = scan_module(item[1])
    return dictionary


def generate_string(dict_or_list: Union[Dict[str, List[types.FunctionType]], List[types.FunctionType]],
                    gen_str: str = None) -> str:
    """
    Generates the string, in markdown. It will generate a string based on the given string format.

    :param dict_or_list: The dictionary or list to generate a string for. If it is a list, the gen_str does not need to
                        have a value, as it will not be used. The format for functions are '%d. `%s`\n', where the first
                        input is the function number, and the second input is the function name.
    :type dict_or_list: Union[Dict[str, List[types.FunctionType]], List[types.FunctionType]]
    :param gen_str: The generation string to use. Any given string format must have two '%s' formats included, where the
                    first one will be the name of the module, and the second one is for the list of functions, which are
                    numbered.
    :type gen_str: str
    :return: The formatted string
    :rtype: str
    """
    formatted_string = ''
    if isinstance(dict_or_list, list):
        count = 0
        for entry in dict_or_list:
            try:
                entry.__name__
            except AttributeError:
                pass
            else:
                count += 1
                print('Found function %s' % entry.__name__)
                formatted_string += '%d. `%s`\n' % (count, entry.__name__)
    elif isinstance(dict_or_list, dict):
        ct = 0
        toc = """# Table of Contents: \n\n"""
        for name, flist in dict_or_list.items():
            print('Found module %s' % name)
            formatted_string += ('\n\n' + gen_str) % (name, generate_string(flist))
            ct += 1
            toc += '%d. [%s](#%s)\n' % (ct, name, name)
        formatted_string = toc.rstrip() + formatted_string
    return formatted_string.strip()


if __name__ == '__main__':
    """
    This main function will generate the 'DIRECTORY.md' file for the module package Geometry.
    """
    geo = generate_directory(Geometry)

    MODULE_FORMAT = """# %s

## Functions:

%s

    """.strip()
    with open('DIRECTORY.md', 'w') as file:
        file.write(generate_string(geo, gen_str=MODULE_FORMAT))
