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
from packaging import version

from scripts import settings
from scripts.layout import layout, info_popup, role_images_finder, layout_settings

# TODO: Adding a way to change themes
#
# maybe add the following:

# light: Reddit, LightGrey, LightBlue
# dark: DarkGrey11 (Default), PythonPlus, Topanga
# darkest: NeonYellow1, NeonBlue1, NeonGreen1
# other: DarkRed, HotDogStand, BrightColors
sg.theme_global("DarkGrey11")


class Global:

    def __init__(self):
        # API
        self.request_available = None

        # Double Click
        self.time_is_running = False
        self.start_timer = "ERROR"

        # rotation
        self.rotation = settings.get_setting("config.json", "rotation")
        self.parsed_rotation = self.role_limiter()

        self.last_selected = "quick"
        self.limiting = []

        # Version
        self.str_version = "1.2.0-beta01"
        self.version = version.parse(self.str_version)  # v1.2.0-beta01

        self.checked_version = False

    def compare_version(self, test_version: str, file_name: str) -> tuple[bool, bool]:
        """
        Checks if the program Version matches the given Version
        :param file_name: Is used in the popup when the given Version is newer than the program Version
        :param test_version: The Version to compare. Assumes the Format: vX.X.X (v1.1.0) or vX.X.X-X (v1.1.0-beta01)
        :return: If the Version matches.
        """
        if self.checked_version:
            return True, True

        test_str_version = test_version
        test_version = version.parse(test_version)

        if test_version > self.version:
            yes_no = sg.popup_yes_no(f"The Version of the {file_name} v{test_str_version} is newer than "
                                     f"the program version (v{self.str_version})\nThis could cause Problems\nTry anyways?")

            if yes_no == "Yes":
                test_version = self.version

        self.checked_version = True
        return test_version == self.version, test_version > self.version

    def _requests_available(self) -> None:

        try:
            import requests

        except ImportError:
            self.request_available = False

        finally:
            self.request_available = True

    def double_click(self):
        if not self.time_is_running:
            self.start_timer = time.time()
            self.time_is_running = True

        elif self.time_is_running:
            end = time.time()
            self.time_is_running = False

            return end - self.start_timer <= 0.2

        self.start_timer = time.time()

    def role_string_parsing(self, string: str):
        return string.replace("-", " ").removesuffix("human")


    def role_limiter(self, selected: str = "quick"):
        layout = []
        frame_layout = []
        number = 0
        group_number = 0

        for k in self.rotation.keys():
            for item in self.rotation[k]:
                if isinstance(item, list):
                    radio_group = []
                    for option in item:
                        option = self.role_string_parsing(", ".join(option))

                        radio_group.append(
                            sg.Radio(option, group_id=f"{k}_{number}_radio", key=f"{k}_{number}_{group_number}_radio",
                                     default=group_number == 0))

                        group_number = group_number + 1

                    frame_layout.append(radio_group)

                    number = number + 1
                else:
                    item: str = item

                    frame_layout.append([sg.Text(self.role_string_parsing(item))])

                group_number = 0
            number = 0

            layout.append(sg.Frame(title="", layout=frame_layout, visible=selected == k, key=k, border_width=0))
            frame_layout = []

        return layout

    def __str__(self):
        return self.str_version




States = Global()


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


def get_image_path(image: str) -> str | bool:
    """
    Returns the full path to an image based on the provided image name.

    :param image: The name of the image (e.g., "evil", "good", "unchecked").
    :return: The full path to the image file. False if the file is not found

    """
    if image.strip() in image_path:
        return image_path[image]

    else:
        if image.strip() in role_path:
            return role_path[image]

        else:
            settings.raise_error(f"The Image for {image} was not found\nPlease check if the file is in the right Place")
            return False


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
        Opens a settings window where the user can change settings like player names and reset the game state.
        """

        def change_selected_limiter(changing: str):
            w1[States.last_selected].update(visible=False)
            w1[changing].update(visible=True)
            States.last_selected = changing

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

            # API settings

            if event_settings == "dropie":
                change_selected_limiter(value_settings["dropie"])

            elif event_settings == "activator" and value_settings["activator"]:
                number = 0

                for i in States.rotation[value_settings["dropie"]]:

                    if isinstance(i, str):
                        States.limiting.append(States.role_string_parsing(i))
                    elif isinstance(i, list):
                        for k in range(len(i)):
                            radio_key = f"{value_settings['dropie']}_{number}_{k}_radio"

                            if radio_key in value_settings and value_settings[radio_key]:
                                if len(i[k]) <= 2:
                                    for y in i[k]:
                                        States.limiting.append(States.role_string_parsing(y))
                                else:
                                    States.limiting.append(States.role_string_parsing(i[k]))

                        number += 1

                    else:
                        print("WAS??")
                w["role_picker"].update(values=States.limiting)

            elif event_settings == "activator" and not value_settings["activator"]:
                States.limiting = []


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
                i: str = i
                if States.limiting:
                    if i in States.limiting and value_main["search_bar"] in i:
                        print(i)
                        role_liste.append(i)

                elif value_main["search_bar"] in i:
                    role_liste.append(i)

                w["role_picker"].update(role_liste)


        elif event_main[-3:] == "but":
            set_value = ""

            double_click = States.double_click()

            for i in choose_possibility:
                if double_click:
                    set_value = team["dead"]

                    break

                elif value_main[f"choose {i}"]:
                    set_value = i

                    break

            if value_main[f"choose {team["specific"]}"] and not double_click:
                if value_main["role_picker"]:
                    set_value = value_main["role_picker"][0]

                else:
                    set_value = None


            if set_value:
                image = get_image_path(image=set_value)

                if image:
                    w[event_main].update(image_source=image)

                    event_main = event_main.split(" ")

                    event_main: int = int(event_main[0]) + int(event_main[1])

                    team_dict[event_main] = set_value

                    w["info left"](get_unchecked())
                    set_value = ""
