# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import FreeSimpleGUI as sg
import webbrowser as wb
import os

from scripts import settings


def layout() -> list:
    """
    Generates the entire main layout.
    :return: A list with sg.elements.
    """
    from main import trans, choose_possibility, get_unchecked

    # adding the menu bar
    menutrans = trans["settings"]
    menu_def = [[menutrans["generel"], [menutrans["info"], menutrans["settings"], menutrans["exit"]]]]
    liste = [[sg.MenuBar(menu_definition=menu_def)]]

    # arranging a 4x4 field for every Player and setting the Unchecked image as default
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(
                sg.Frame(title=f"{i + k}. {trans["player"]}", key=f"{i} {k} frame", element_justification="center",
                         layout=[[sg.Button(image_source="images/generic/unchecked.png", key=f"{i} {k} but")],
                                 [sg.Input(key=f"{i} {k} info", size=(14, None))]]))

    adding_list = []

    # Adding the radio buttons, the search bar, and arranging them into 2 rows
    for i in choose_possibility:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}", default=choose_possibility[0] == i))

    len_adding_list = int(len(adding_list) / 2) + 1
    adding_list.append(sg.Input(key="search_bar", size=26, enable_events=True))

    adding_list = [adding_list[:len_adding_list + 1], adding_list[len_adding_list + 1:]]

    # Adding the box for selecting the role
    liste.append([sg.Frame(title="", layout=adding_list, element_justification="center"),
                  sg.Listbox(role_images_finder(), size=(25, 4), key="role_picker")])

    # The remaining people bar
    liste.append([sg.Input(size=71, key="info left", default_text=get_unchecked())])

    return liste


def role_images_finder(path: str = "images/roles", full_path=False) -> list | dict:
    """
    Searches the given path for all .png and .jpg files and adds them to the return.
    :param path: The path to search (default: images/roles).
    :param full_path: If True, the full path to the image is returned. If False, only the name is returned.
    :return: If full_path is False, the name without the file extension is returned in a list (e.g., "villager.png" -> "villager"). If full_path is True, the path from the repo root is returned (e.g., "images/roles/village/villager.png").
    """
    file_name_list = []
    path_list = {}

    settings.check_for_file(path)

    for root, directories, files in os.walk(path):
        for dateiname in files:
            if dateiname.endswith(".jpg") or dateiname.endswith(".png"):

                if full_path:
                    path_list[dateiname[:-4]] = root + "/" + dateiname
                else:
                    file_name_list.append(dateiname[:-4])

    if full_path:
        return path_list

    else:
        file_name_list.sort()
        return file_name_list


def layout_settings() -> list:
    """
    Generates the layout for the settings window.
    :return: A list with sg.elements.
    """
    from main import trans

    set_trans = trans["settings"]

    # General Tab
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(set_trans["change_names"], key="name_key")])

    name_layout = sg.Frame(title=set_trans["names"], layout=liste)

    language, selected = settings.get_available_languages()

    game_layout = [[sg.T(set_trans["language"])],
                   [sg.Combo(key="language", values=language, default_value=selected, enable_events=True)]]

    game_layout = sg.Frame(title=set_trans["games_settings"], layout=game_layout)

    reset_layout = sg.Frame(title=set_trans["reset_name"],
                            layout=[[sg.Button(set_trans["reset"], key="reset")],
                                    [sg.Button(set_trans["reset_name"], key="reset-name")],
                                    [sg.Button(set_trans["reset_all"], key="reset_all")]])

    reset_layout = sg.Frame(title=trans["settings"]["reset_name"],
                            layout=[[sg.Button(trans["settings"]["reset"], key="reset")],
                                    [sg.Button(trans["settings"]["reset_name"], key="reset-name")],
                                    [sg.Button(trans["settings"]["reset_all"], key="reset_all")]])

    return [[name_layout], [game_layout, reset_layout]]


def info_popup() -> None:
    from main import States
    """
    Opens a popup-like window with general information about the program (e.g., version, license, source code location, and more).
    """
    layout = [[sg.Frame(title="Program Information", layout=[[sg.T("This Program is not related with Wolvesville")],
                                                             [sg.T("This Program is licensed under the GNU GPL v3")],
                                                             [sg.Button("Read the Full License", key="full")],
                                                             [sg.T("The Source Code can be found on GitHub")],
                                                             [sg.Button("Open the GitHub projekt", key="github")],
                                                             [sg.T(
                                                                 "All images in the images order have been downloaded \n"
                                                                 "via the official Wolvesville API \n"
                                                                 "With the exception of the generic order \n"
                                                                 "these come from the Wolvesville Wiki ")],
                                                             [sg.Button("Wolvesville API", key="API"),
                                                              sg.Button("Wolvesville Wiki", key="wiki")],
                                                             [sg.T(str(States))], ])],
              [sg.Button("Close", key="close")]]

    w1 = sg.Window(title="Info", layout=layout, keep_on_top=True)

    while True:
        event_popup, v = w1.read()

        if event_popup is None or event_popup == "close":
            w1.close()
            break

        elif event_popup == "full":
            wb.open(url="https://www.gnu.org/licenses/gpl-3.0")

        elif event_popup == "github":
            wb.open(url="https://github.com/Platzhalten/Wolvlist")

        elif event_popup == "API":
            wb.open(url="https://api-docs.wolvesville.com/#/")

        elif event_popup == "wiki":
            wb.open(url="https://wolvesville.fandom.com/wiki/Wolvesville_Wiki")
