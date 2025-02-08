# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import FreeSimpleGUI as sg
import webbrowser
import os

from scripts import settings


def entire_layout():
    tab1 = sg.Tab(title="Game", layout=layout())
    tab2 = sg.Tab(title="Settings", layout=layout_settings())

    tab = [[sg.TabGroup(layout=[[tab1, tab2]])]]

    return tab


def layout():
    from main import trans, choose_posibily, get_unchecked
    menutrans = trans["settings"]

    menu_def = [[menutrans["generel"], [menutrans["info"], menutrans["exit"]]]]

    liste = [[sg.MenuBar(menu_definition=menu_def)]]
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(sg.Frame(title=f"{i + k}. {trans["player"]}", key=f"{i} {k} frame",
                                      element_justification="center", layout=[
                    [sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")],
                    [sg.Input(key=f"{i} {k} info", size=(14, None))]]))

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}", default=choose_posibily[0] == i))

    len_adding_list = int(len(adding_list) / 2) + 1

    adding_list.append(sg.Input(key="search_bar", size=26, enable_events=True))

    adding_list = [adding_list[:len_adding_list + 1], adding_list[len_adding_list + 1:]]

    liste.append([sg.Frame(title="", layout=adding_list, element_justification="center"),
                  sg.Listbox(role_images_finder(), size=(10, 4), key="role_picker")])

    liste.append([sg.Input(size=75, key="info left", default_text=get_unchecked())])

    return liste


def role_images_finder(path: str = "images/roles"):
    dateinamen_liste = []
    settings.check_for_file("images files", path)

    for root, directories, files in os.walk(path):
        for dateiname in files:
            dateinamen_liste.append(dateiname[:-4])

    return dateinamen_liste


def layout_settings():
    from main import trans, voting_roles

    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(trans["settings"]["change_names"], key="name_key")])

    name_layout = sg.Frame(title=trans["settings"]["names"], layout=liste)

    language = settings.get_avaible_languages()

    game_layout = [[sg.T(trans["settings"]["language"])],
                   [sg.Combo(key="lang", values=language[0], default_value=language[1], enable_events=True)],
                   [sg.T(trans["what_voting_role"])],
                   [sg.Combo(key="narr", values=voting_roles)]]

    game_layout = sg.Frame(title=trans["settings"]["games_settings"], layout=game_layout)

    reset_layout = sg.Frame(title=trans["settings"]["reset_name"],
                            layout=[[sg.Button(trans["settings"]["reset"], key="reset")],
                                    [sg.Button(trans["settings"]["reset_name"], key="reset-name")],
                                    [sg.Button(trans["settings"]["reset_all"], key="reset_all")]])

    return [[name_layout], [game_layout, reset_layout]]


def info_popup():
    layout = [[sg.Frame(title="Program Information", layout=[[sg.T("This Program is licensed under the GNU GPL v3")],
                                                             [sg.Button("Read the Full License", key="full")],
                                                             [sg.T("The Source Code can be found on GitHub")],
                                                             [sg.Button("Open the GitHub projekt", key="github")],
                                                             [sg.T("v1.1.0-beta.01")]])],
              [sg.Button("Close", key="close")]]

    w1 = sg.Window(title="Info", layout=layout, keep_on_top=True)

    while True:
        e, v = w1.read()

        if e is None or e == "close":
            w1.close()
            break

        elif e == "full":
            webbrowser.open(url="https://www.gnu.org/licenses/gpl-3.0")

        elif e == "github":
            webbrowser.open(url="https://github.com/Platzhalten/Wolvlist")
