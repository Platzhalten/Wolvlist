# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import json
import os
import FreeSimpleGUI as sg


def get_available_languages() -> list:
    """
    :return: a list with 2 elements the first one is a list with all available languages (excluding the selected language) and the second one is the currently selected
    """
    check_for_file(path="lang.json")

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    liste = []

    for i in f:
        if not i == "selected":

            liste.append(f"{i} - {f[i]["language_full_name"]}")

    return [liste, f["selected"]]


def get_language(language: str = None) -> dict:
    """
    Returns the language dictionary for the specified or selected language
    :param language: The language that dict should have. If None is set the selected language is used
    :return: a dict with all the strings, when a string is not available in the selected languages its get replace with the english string
    """
    check_for_file(path="lang.json")

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    if language is None:
        language = f["selected"]

    return merge_dictionaries(f["en"], f[language[0:2]])


def merge_dictionaries(dict1, dict2) -> dict:
    """
    Replaces the values of dict1 with the value from dict2 if they exist
    :param dict1: The bigger one
    :param dict2: The smaller dict
    :return: a merged dict
    """
    merged_dict = dict2.copy()

    for key, value in dict1.items():
        if key not in merged_dict:

            merged_dict[key] = value
        elif isinstance(value, dict) and isinstance(merged_dict[key], dict):
            merged_dict[key] = merge_dictionaries(value, merged_dict[key])

    return merged_dict


def change_selected_lang(language: str) -> None:
    """
    Changes the default Languages
    :param language: what language it should be
    """

    check_for_file("lang.json")

    with open("lang.json", "r") as f:

        l = json.loads(f.read())

        l["selected"] = language

    with open("lang.json", "w") as f:
        f.write(json.dumps(l, indent=3))


def check_for_file(path: str, leave: bool = True) -> bool:
    """
    Checks if a path is valid and creates a popup informing the User
    :param path: the path to check
    :param leave: should the program exit if the path is not valid
    :return: if the path exist
    """
    if os.path.exists(path):
        return True

    else:
        error_message = (f"The File or Directory {path} is missing.\n"
                         f"You need one to run the Program you can find one on the Github of this Projekt: https://github.com/Platzhalten/Wolvlist/\n"
                         f"Then place it in the same place like the main.py\n")

        if leave:
            error_message = error_message + f"The Program is exiting now"

            sg.popup_error(error_message)
            exit()
        else:
            sg.popup_error(error_message)

        return False
