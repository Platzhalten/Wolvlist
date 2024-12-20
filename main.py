
#  Copyright (C) 2024 Eric M.
#
#   The Complet License is in LICENSE
#
#   This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

# GLOBAL VARIABEL
choosen = None

image_path = {
    "böse": "images/generic/Evil.png",
    "gut": "images/generic/Good.png",
    "unchecked": "images/generic/Unchecked.png",
    "ubk": "images/generic/Unknown.png",
    "Narr/HH": "images/voting/Generic.png",
    "Anarchist": "images/voting/Anarchist.png",
    "Narr": "images/voting/Fool.png",
    "hh": "images/voting/Headhunter.png",
    "dead": "images/generic/dead.png"
}

# OPTION

voting_roles = ["Narr", "hh", "Anarchist"]
choose_posibily = ["gut", "ubk", "böse", "Narr/HH", "unchecked", "dead"]

team_dict = dict.fromkeys(range(1,17), "unchecked")


def get_image_path(image: str):
    return image_path[image]


def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(sg.Frame(title=f"{i + k}. Player", size=(125, 125), layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but", metadata="Unchecked")]]))

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}"))

    liste.append(adding_list)


    liste.append([sg.Input(size=116)])
    liste.append([sg.Input(size=116, key="info out")])
    liste.append([sg.Input(size=116, key="info left")])


    liste.append([sg.T("Welche voting role ig: "), sg.Combo(key="narr", values=voting_roles)])

    return liste


def layout_2():
    name_layout = []
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. Player", key=f"{i} name")])

    liste.append([sg.Button("add the names", key="name_key")])

    name_layout.append(sg.Frame(title="Names", layout=liste))



    game_layout = [[sg.T("Welche Voting Roles gibt es")]]

    game_layout = [[sg.Frame(title="Game Settings", layout=game_layout)]]


    return [name_layout]


def get_extra_info():
    pass


def layout_settings():
    return [[sg.T("At the Moment there are no Settings here")]
    ]

tab1 = sg.Tab(title="Game", layout=layout())
tab2 = sg.Tab(title="Settings", layout=layout_2())


tab = [[sg.TabGroup(layout=[[tab1, tab2]])]]

w = sg.Window(title="werville", layout=tab, resizable=True)

while True:

    e, v = w.read()

    e: str = e

    if e is None:
        w.close()
        break

    if e == "name_key":
        for i in range(1,17):

            w[f"{i}.1"](v[f"{i} name"])



    if e[-3:] == "but":
        set_value = ""

        for i in choose_posibily:
            if v[f"choose {i}"]:
                set_value = i

                break

        if set_value:
            if v["narr"] and set_value == "Narr/HH":
                set_value = v["narr"]

            w[e].update(image_source=get_image_path(image=set_value))

            e = e.split(" ")

            e: int = int(e[0]) + int(e[1])

            team_dict[e] = set_value


            unchecked = ""


            for i in team_dict:

                if team_dict[i] == "unchecked":
                    unchecked += (str(i) + " ")


            unchecked += "übrig"

            w["info left"](unchecked)

            set_value = ""
