#  Copyright (C) 2025 Eric M.
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
import time

from scripts import settings
from scripts.layout import entire_layout, info_popup, role_images_finder

sg.theme_global("DarkGrey11")


# GLOBAL VARIABEL
choosen = None
times = False
start = "ERROR"
override = False
temp = 0

trans = settings.get_language()
team = trans["team_selector"]
role = trans["roles"]

image_path = {
    team["evil"]: "images/generic/Evil.png",
    team["good"]: "images/generic/Good.png",
    team["unchecked"]: "images/generic/Unchecked.png",
    team["unknown"]: "images/generic/Unknown.png",
    team["voting_role"]: "images/generic/voting.png",
    team["dead"]: "images/generic/dead.png",
}

# OPTION
voting_roles = [role["fool"], role["headhunter"], role["anarchist"]]
choose_posibily = [team["good"], team["unknown"], team["evil"], team["unchecked"], team["specific"]]

team_dict = dict.fromkeys(range(1,17), team["unchecked"])


def get_image_path(image: str):
    if image in image_path:
        return image_path[image]

    else:
        return f"images/roles/{image}.png"


def get_unchecked():
    unchecked = ""
    for i in team_dict:

        if team_dict[i] == "unchecked":
            unchecked += (str(i) + " ")

    unchecked += trans["left"]

    return unchecked


def all_player():
    for colum in range(1, 17, 4):
        for row in range(0, 4):
            yield colum, row


if __name__ == '__main__':

    w = sg.Window(title="werville", layout=entire_layout(), finalize=True)

    while True:

        e, v = w.read()

        if e is None or e == "exit":
            w.close()
            break

        e: str = e

        if e == "Info":
            info_popup()

        elif e == "name_key":

            for i, k in all_player():
                w[f"{i} {k} frame"](v[f"{i + k} name"])

        elif e.startswith("reset"):
            conf = sg.popup_yes_no(trans["settings"]["conformation"])

            if conf == "Yes":
                team_dict = dict.fromkeys(range(1, 17), team["unchecked"])

                if e == "reset-name" or e == "reset_all":
                    for i in range(1, 17):
                        w[f"{i} name"].update(f"{i}. {trans["player"]}")

                if e == "reset" or e == "reset_all":
                    w["info left"].update(get_unchecked())

                for i, k in all_player():
                    if e == "reset-name":
                        w[f"{i} {k} frame"].update(f"{i + k} {trans["player"]}")

                    elif e == "reset_all":
                        w[f"{i} {k} frame"].update(f"{i + k} {trans["player"]}")
                        w[f"{i} {k} but"].update(image_source=get_image_path(image=team["unchecked"]))
                        w[f"{i} {k} info"].update("")

                    else:
                        w[f"{i} {k} but"].update(image_source=get_image_path(image=team["unchecked"]))
                        w[f"{i} {k} info"].update("")


        elif e == "search_bar":
            role_liste = []

            for i in role_images_finder():
                if v["search_bar"] in i:
                    role_liste.append(i)

                w["role_picker"].update(role_liste)


        elif e[-3:] == "but":
            set_value = ""

            if not times:
                start = time.time()
                times = True
                override = False
                temp = e

            elif times:
                end = time.time()

                if end - start <= 0.2:
                    override = True
                    times = False

            start = time.time()

            for i in choose_posibily:
                if override:
                    set_value = team["dead"]

                    break

                elif v[f"choose {i}"]:
                    set_value = i

                    break

            if v[f"choose {team["specific"]}"] and not override:
                if v["role_picker"]:
                    set_value = v["role_picker"][0]

                else:
                    set_value = None


            if set_value:
                w[e].update(image_source=get_image_path(image=set_value))

                e = e.split(" ")

                e: int = int(e[0]) + int(e[1])

                team_dict[e] = set_value

                w["info left"](get_unchecked())
                set_value = ""

        elif e == "lang":
            settings.change_selected_lang(v["lang"][0:3].strip())
