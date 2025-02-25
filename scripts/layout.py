# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import FreeSimpleGUI as sg
import webbrowser as wb
import os

from scripts import settings


def layout():
    """
    Generates the entire main layout
    :return: a list with sg.elements
    """
    from main import trans, choose_posibily, get_unchecked

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
                         layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")],
                                 [sg.Input(key=f"{i} {k} info", size=(14, None))]]))

    adding_list = []

    # adding the radio buttons, the search bar and move then into 2 rows
    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}", default=choose_posibily[0] == i))

    len_adding_list = int(len(adding_list) / 2) + 1
    adding_list.append(sg.Input(key="search_bar", size=26, enable_events=True))

    adding_list = [adding_list[:len_adding_list + 1], adding_list[len_adding_list + 1:]]

    # added the box for selecting the role
    liste.append([sg.Frame(title="", layout=adding_list, element_justification="center"),
                  sg.Listbox(role_images_finder(), size=(25, 4), key="role_picker")])

    # the remaining people bar
    liste.append([sg.Input(size=71, key="info left", default_text=get_unchecked())])

    return liste


def role_images_finder(path: str = "images/roles", full_path=False):
    """
    Searches the given path for all .png and .jpg files and adding then to the return
    :param path: the path where to search default: images/roles
    :param full_path: if the full path to the image should be return or only the name
    :return: if full_path is False then the name without the file exteions will be returnt in a list (villager.png > villager) when full_path is True then the path from the repo root (images/roles/village/villager.png)
    """
    dateinamen_liste = []
    path_list = {}

    settings.check_for_file(path)

    for root, directories, files in os.walk(path):
        for dateiname in files:
            if dateiname.endswith(".jpg") or dateiname.endswith(".png"):

                if full_path:
                    path_list[dateiname[:-4]] = root + "/" + dateiname
                else:
                    dateinamen_liste.append(dateiname[:-4])

    if full_path:
        return path_list

    else:
        dateinamen_liste.sort()
        return dateinamen_liste



def layout_settings():
    from main import trans

    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(trans["settings"]["change_names"], key="name_key")])

    name_layout = sg.Frame(title=trans["settings"]["names"], layout=liste)

    language = settings.get_available_languages()

    game_layout = [[sg.T(trans["settings"]["language"])],
                   [sg.Combo(key="language", values=language[0], default_value=language[1], enable_events=True)]]

    game_layout = sg.Frame(title=trans["settings"]["games_settings"], layout=game_layout)

    reset_layout = sg.Frame(title=trans["settings"]["reset_name"],
                            layout=[[sg.Button(trans["settings"]["reset"], key="reset")],
                                    [sg.Button(trans["settings"]["reset_name"], key="reset-name")],
                                    [sg.Button(trans["settings"]["reset_all"], key="reset_all")]])

    return [[name_layout], [game_layout, reset_layout]]


def info_popup() -> None:
    """
    Opens a Popup like window with general infos about the Program (e.g. the Version, the License, where to find the source code and some more)
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
                                                             [sg.T("v1.1.0-beta.03")], ])],
              [sg.Button("Close", key="close")]]

    w1 = sg.Window(title="Info", layout=layout, keep_on_top=True)

    while True:
        e, v = w1.read()

        if e is None or e == "close":
            w1.close()
            break

        elif e == "full":
            wb.open(url="https://www.gnu.org/licenses/gpl-3.0")

        elif e == "github":
            wb.open(url="https://github.com/Platzhalten/Wolvlist")

        elif e == "API":
            wb.open(url="https://api-docs.wolvesville.com/#/")

        elif e == "wiki":
            wb.open(url="https://wolvesville.fandom.com/wiki/Wolvesville_Wiki")
