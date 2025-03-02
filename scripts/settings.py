# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import json
import os
import FreeSimpleGUI as sg


def set_settings(path: str, setting: str, value: str) -> None:
    original = get_setting(path)

    original[setting] = value

    with open(path, "w") as f:
        f.write(json.dumps(original))


def get_available_languages() -> tuple[list[str], str]:
    """
    :return: a list with 2 elements the first one is a list with all available languages (excluding the selected language) and the second one is the currently selected
    """
    check_for_file(path="lang.json")

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    liste = []

    selected = "ERROR"

    for i in f:
        if not i == "selected":
            liste.append(f"{i} - {f[i]["language_full_name"]}")

        else:
            selected = f["selected"]
            selected = f"{f["selected"]} - {f[selected]["language_full_name"]}"

    return liste, selected


def get_language(language: str = None) -> dict:
    """
    Returns the language dictionary for the specified or selected language
    :param language: The language code (e.g., "en", "de"). If None, the currently selected language is used.
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
    Merges two dictionaries, with values from `dict2` overriding those in `dict1`.

    :param dict1: The base dictionary.
    :param dict2: The dictionary whose values will override those in `dict1`.
    :return: A new dictionary containing the merged data.
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
    :param language: the language code (e.g. "en", "de")
    """

    check_for_file("lang.json")

    with open("lang.json", "r") as f:

        l = json.loads(f.read())

        l["selected"] = language

    with open("lang.json", "w") as f:
        f.write(json.dumps(l, indent=3))


def check_for_file(path: str, leave: bool = True) -> bool:
    """
    Checks if a file or directory exists. A popup is created when the file or directory does not exist informing the User
    :param path: the path to check
    :param leave: should the program exit if the path is not valid. No PopUp is show when False
    :return: True when the Path exist, False otherwise
    """
    if os.path.exists(path):
        return True

    else:
        if not leave:
            return False

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
