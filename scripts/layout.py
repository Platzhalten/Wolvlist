# Copyright (C) 2025 Eric M.
#
# full license at ../LICENSE

import FreeSimpleGUI as sg
import webbrowser

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
            liste[-1].append(sg.Frame(title=f"{i + k}. {trans["player"]}", key=f"{i} {k} frame", size=(125, 125),
                                      element_justification="center", layout=[
                    [sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")]]))

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}", default=choose_posibily[0] == i))

    liste.append(adding_list)

    liste.append([sg.Input(size=75, key="info out")])
    liste.append([sg.Input(size=75, key="info left", default_text=get_unchecked())])

    return liste


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
                                                             [sg.Button("Open the GitHub projekt", key="github")]])],
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
