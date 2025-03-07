# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import json
import os
import FreeSimpleGUI as sg


def get_setting(path: str, setting: str = None) -> dict:
    """
    Reads the JSON file at the path and returns parts/the entire content.
    :param path: The path to the JSON file.
    :param setting: The setting to return (a dict path). If None, the entire JSON file is returned.
    :return: The content of the JSON file.
    """
    check_for_file(path)

    with open(path, "r") as f:
        f = f.read()

        try:
            if setting is None:
                return json.loads(f)

            elif json.loads(f)[setting]:
                return json.loads(f)[setting]

        except KeyError:
            return {}


def set_settings(path: str, setting: str, value: str) -> None:
    """
    Gets the content of the path, changes the values, and writes the changed content to the same path.
    :param path: The path to the JSON file.
    :param setting: The setting to change (key).
    :param value: The value of the setting.
    """
    original = get_setting(path)

    original[setting] = value

    with open(path, "w") as f:
        f.write(json.dumps(original, indent=3))


def get_available_languages() -> tuple[list[str], str]:
    """
    :return: A list with 2 elements: the first is a list of all available languages (excluding the selected language), and the second is the currently selected language.
    """
    language = get_setting("lang.json")

    liste = []

    selected = get_setting("config.json", "language")

    for i in language:
        liste.append(f"{i} - {language[i]["language_full_name"]}")

        if i.startswith(selected):
            selected = f"{selected} - {language[i]["language_full_name"]}"

    return liste, selected


def get_language(language: str = None) -> dict:
    """
    Returns the language dictionary for the specified or selected language
    :param language: The language code (e.g., "en", "de"). If None, the currently selected language is used.
    :return: A dict with all the strings. If a string is not available in the selected language, it is replaced with the English string.
    """
    from main import States

    f = get_setting("lang.json")

    try:
        matching = States.compare_version(f["en"]["version"], file_name="lang.json")
        if matching is None:
            raise ValueError
        elif not matching:
            raise KeyError

    except KeyError as e:
        wrong_version = "The Version of the lang.json is older than the Version of the Program \nPlease get a matching or newer Version"

        sg.popup_error(wrong_version)
        raise Exception(wrong_version)


    if language is None:
        language = get_setting("config.json", "language")

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
    Changes the default Languages.
    :param language: The language code (e.g. "en", "de")
    """
    if len(language) == 2:
        set_settings("config.json", setting="language", value=language)


def check_for_file(path: str, leave: bool = True) -> bool:
    """
    Checks if a file or directory exists. A popup is created if the file or directory does not exist, informing the user.
    :param path: The path to check.
    :param leave: Should the program exit if the path is not valid. No popup is show when False
    :return: True if the Path exist, False otherwise
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
