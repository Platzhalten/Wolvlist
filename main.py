
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
import time

import settings
from layout import entire_layout

sg.theme_global("DarkGrey11")


# GLOBAL VARIABEL
choosen = None
times = False
start = "ERROR"
override = False

trans = settings.get_settings()
team = trans["team_selector"]
role = trans["roles"]

image_path = {
    team["evil"]: "images/generic/Evil.png",
    team["good"]: "images/generic/Good.png",
    team["unchecked"]: "images/generic/Unchecked.png",
    team["unknown"]: "images/generic/Unknown.png",
    team["voting_role"]: "images/voting/Generic.png",
    role["anarchist"]: "images/voting/Anarchist.png",
    role["fool"]: "images/voting/Fool.png",
    role["headhunter"]: "images/voting/Headhunter.png",
    team["dead"]: "images/generic/dead.png"
}

# OPTION

voting_roles = [role["fool"], role["headhunter"], role["anarchist"]]
choose_posibily = [team["good"], team["unknown"] , team["evil"], team["voting_role"], team["unchecked"]]

team_dict = dict.fromkeys(range(1,17), team["unchecked"])


def get_image_path(image: str):
    return image_path[image]


if __name__ == '__main__':

    w = sg.Window(title="werville", layout=entire_layout(), finalize=True)


    while True:

        e, v = w.read()

        print(e)

        if e is None:
            w.close()
            break

        e: str = e


        if e == "name_key":
            for i in range(1, 17, 4):
                for k in range(0, 4):

                    w[f"{i} {k} frame"](v[f"{i + k} name"])


        elif e[-3:] == "but":
            set_value = ""

            if not times:
                start = time.time()
                times = True
                override = False

            elif times:
                if time.time() - start <= 0.5:
                    override = True
                    times = False

                    set_value = team["dead"]


            for i in choose_posibily:
                if v[f"choose {i}"] and not override:
                    set_value = i

                    break


            if set_value:
                if v["narr"] and set_value == "Narr/hh":
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

        elif e == "lang":
            settings.change_selected_lang(v["lang"][0:3].strip())

