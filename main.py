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
from scripts.layout import layout, info_popup, role_images_finder, layout_settings

sg.theme_global("DarkGrey11")


# GLOBAL VARIABEL
choosen = None
times = False
start = "ERROR"
override = False
temp = 0
version = "v1.1.0"

trans = settings.get_language()
team = trans["team_selector"]
role = trans["roles"]

image_path = {
    team["evil"]: "images/generic/evil.png",
    team["good"]: "images/generic/good.png",
    team["unchecked"]: "images/generic/unchecked.png",
    team["unknown"]: "images/generic/unknown.png",
    team["dead"]: "images/generic/dead.png",
}

# OPTION
choose_possibility = [team["good"], team["unknown"], team["evil"], team["unchecked"], team["specific"]]

team_dict = dict.fromkeys(range(1,17), team["unchecked"])

role_path = role_images_finder(full_path=True)


def get_image_path(image: str) -> str:
    """
    Returns the full path to an image based on the provided image name.

    :param image: The name of the image (e.g., "evil", "good", "unchecked").
    :return:The full path to the image file.

    """
    if image in image_path:
        return image_path[image]

    else:
        return role_path[image]


def get_unchecked() -> str:
    """
    Generates a string listing all players whose team status is "unchecked".

    :return: A string with the number of unchecked players (e.g., "1 2 3 left").
            (depending on the language another word is used for left)
    """
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

    for i in image_path.values():
        settings.check_for_file(path=i)

    w = sg.Window(title="werville", layout=layout(), finalize=True)


    def settings_win():
        """
        Opens a settings Window where the user can change thinks like Player Names and reset the game state
        """

        w1 = sg.Window(title=trans["settings"]["settings"], layout=layout_settings())

        while True:
            event_settings, value_settings = w1.read()

            event_settings: str = event_settings

            if event_settings is None:
                w1.close()
                return

            # General Settings
            elif event_settings == "language":
                settings.change_selected_lang(value_settings["language"][0:3].strip())

            elif event_settings.startswith("reset") and sg.popup_ok_cancel(trans["settings"]["conformation"]) == "OK":

                if event_settings == "reset" or event_settings == "reset_all":
                    w["info left"].update(get_unchecked())

                for i, k in all_player():
                    if event_settings == "reset-name":
                        w[f"{i} {k} frame"].update(f"{i + k}. {trans["player"]}")

                    elif event_settings == "reset_all":
                        w[f"{i} {k} frame"].update(f"{i + k}. {trans["player"]}")
                        w[f"{i} {k} but"].update(image_source=get_image_path(image=team["unchecked"]))
                        w[f"{i} {k} info"].update("")

                    else:
                        w[f"{i} {k} but"].update(image_source=get_image_path(image=team["unchecked"]))
                        w[f"{i} {k} info"].update("")

            elif event_settings == "name_key":
                for i, k in all_player():
                    w[f"{i} {k} frame"](value_settings[f"{i + k} name"])


    while True:

        event_main, value_main = w.read()

        if event_main is None or event_main == "exit":
            w.close()
            break

        event_main: str = event_main

        if event_main == "Info":
            info_popup()

        elif event_main == trans["settings"]["settings"]:
            settings_win()

        elif event_main == "search_bar":
            role_liste = []

            for i in role_images_finder():
                if value_main["search_bar"] in i:
                    role_liste.append(i)

                w["role_picker"].update(role_liste)


        elif event_main[-3:] == "but":
            set_value = ""

            if not times:
                start = time.time()
                times = True
                override = False
                temp = event_main

            elif times:
                end = time.time()

                if end - start <= 0.2:
                    override = True
                    times = False

            start = time.time()

            for i in choose_possibility:
                if override:
                    set_value = team["dead"]

                    break

                elif value_main[f"choose {i}"]:
                    set_value = i

                    break

            if value_main[f"choose {team["specific"]}"] and not override:
                if value_main["role_picker"]:
                    set_value = value_main["role_picker"][0]

                else:
                    set_value = None


            if set_value:
                w[event_main].update(image_source=get_image_path(image=set_value))

                event_main = event_main.split(" ")

                event_main: int = int(event_main[0]) + int(event_main[1])

                team_dict[event_main] = set_value

                w["info left"](get_unchecked())
                set_value = ""

