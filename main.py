#  Copyright (C) 2025 Eric M.
#
#   The Complete License is in LICENSE
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
from time import time
from packaging import version

from scripts import settings
from scripts.layout import layout, info_popup, role_images_finder, layout_settings


class Global:

    def __init__(self):
        # General
        self.team_dict = dict.fromkeys(range(1, 17), "unchecked")

        # API
        self.API = None

        self.API_available = False
        self.API_key_available = False

        self.request_available = self._requests_available()

        self.enable_api(settings.get_setting("config.json", "api_key"))

        # Double Click
        self.last_click_button = None
        self.last_click_time = 0

        # rotation
        self.rotation = settings.get_setting("config.json", "rotation")
        self.last_selected = "quick"
        self.parsed_rotation = self.role_limiter()

        self.limiting = []

        # Version
        self.str_version = "1.2.0-beta02"
        self.version = version.parse(self.str_version)

        self.checked_version = False

        # Info bar
        self.current_info = "remaining"  # can be one of remaining and discovered. remaining=1,4 left; discovered=1 good | 3 ubk

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

    def _requests_available(self) -> bool:

        try:
            import requests

        except ImportError:
            return False

        if settings.check_for_file("./scripts/API.py", leave=False, do_not_ask=True):
            self.API_available = True

            if settings.get_setting("config.json", "api_key_is_valid"):
                self.API_key_available = True

        return True

    def enable_api(self, key: str):
        if self.API_available and self.request_available:
            from scripts import API

            if not key:
                return False

            self.API = API.Api(key.removesuffix("\n").strip())

            if not bool(self.API):
                self.API = None
                return False

        return True

    def double_click(self, button):
        current_time = time()
        if self.last_click_button == button and (current_time - self.last_click_time) <= 0.2:
            self.last_click_button = None
            self.last_click_time = 0
            return True
        else:
            self.last_click_button = button
            self.last_click_time = current_time
            return False

    def role_string_parsing(self, string: str):
        return string.replace("-", " ").removesuffix("human")

    def role_limiter(self, selected: str = None):
        layout = []
        frame_layout = []
        number = 0
        group_number = 0
        if selected is None:
            selected = self.last_selected

        for k in self.rotation.keys():
            for item in self.rotation[k]:
                if isinstance(item, list):
                    radio_group = []
                    for option in item:
                        if isinstance(option, str):
                            option = self.role_string_parsing(option)
                        else:
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

    def info_bar(self) -> str:
        if self.current_info == "remaining":
            return get_unchecked()

        elif self.current_info == "discovered":
            return get_checked()

        else:
            return "UNKNOWN TYPE"

    def __str__(self):
        return self.str_version


States = Global()

trans = settings.get_language()
team = trans["team_selector"]
role = trans["roles"]

generic_path: dict = settings.get_setting("config.json", "paths")["generic"]

image_path = {
    team["evil"]: generic_path["evil"],  # default Value: images/generic/evil.png
    team["good"]: generic_path["good"],  # default Value: images/generic/good.png
    team["unchecked"]: generic_path["unchecked"],  # default Value: images/generic/unchecked.png
    team["unknown"]: generic_path["unknown"],  # default Value: images/generic/unknown.png
    team["dead"]: generic_path["dead"],  # default Value: images/generic/dead.png
}

# OPTION
choose_possibility = [team["good"], team["unknown"], team["evil"], team["unchecked"], team["specific"]]
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
    team_trans = trans["team_selector"]
    for i in States.team_dict:

        if States.team_dict[i] == team_trans["unchecked"]:
            unchecked += (str(i) + " ")

    unchecked += trans["left"]

    return unchecked


def get_checked(separator: str = "|") -> str:
    """
    Gets all the players whose team status is "checked".
    :param separator: The separator between roles.
    :return: a string with all checked players and there role (e.g., "1 3 Good | 2 Evil | 5 Doctor)
    """
    team_trans = trans["team_selector"]

    checked = ""
    role_dict = {
        team_trans["good"]: [],
        team_trans["unknown"]: [],
        team_trans["evil"]: [],
    }

    for i in States.team_dict.keys():
        if States.team_dict[i] in role_dict:
            role_dict[States.team_dict[i]].append(str(i))

        elif not States.team_dict[i] in [team_trans["unchecked"], team_trans["dead"]]:
            role_dict[States.team_dict[i]] = [str(i)]

    for i in role_dict:
        if not role_dict[i]:
            continue

        if not checked == "":
            checked = f"{checked} {separator} "

        role_dict[i].append(i)

        checked = checked + (" ".join(role_dict[i]))

    if checked.strip() == "":
        return "NO INFO"

    return checked


def all_player():
    for colum in range(1, 17, 4):
        for row in range(0, 4):
            yield colum, row


def reset(reseting: str = None) -> None:
    """
    Reset the board
    :param reseting: must be one of: name, all, info, if None info is assumed
    :return: None
    """
    for i, k in all_player():
        if reseting == "name":
            main_window[f"{i} {k} frame"].update(f"{i + k}. {trans["player"]}")
            continue

        elif reseting == "all":
            main_window[f"{i} {k} frame"].update(f"{i + k}. {trans["player"]}")

        main_window[f"{i} {k} but"].update(image_source=get_image_path(image=team["unchecked"]))
        main_window[f"{i} {k} info"].update("")
        States.team_dict = dict.fromkeys(range(1, 17), team["unchecked"])

    main_window["info left"].update(get_unchecked())


if __name__ == '__main__':

    for i in image_path.values():
        settings.check_for_file(path=i)

    main_window = sg.Window(title="Wolvlist", layout=layout(), finalize=True, resizable=True)
    main_window.set_min_size(main_window.size)

    States.team_dict.fromkeys(range(1, 17), team["unchecked"])


    def settings_win():
        """
        Opens a settings window where the user can change settings like player names and reset the game state.
        """

        def change_selected_limiter(changing: str):
            settings_window[States.last_selected].update(visible=False)
            settings_window[changing].update(visible=True)
            States.last_selected = changing

        def add_limiting(changing, include_advanced: bool):
            States.limiting.append(States.role_string_parsing(changing))

            if include_advanced:
                if changing == "red-lady":
                    changing = "harlot"

                if changing not in advanced_roles:
                    advanced_roles[changing] = []

                for k in advanced_roles[changing]:
                    States.limiting.append(States.role_string_parsing(k))

        settings_window = sg.Window(title=trans["settings"]["settings"], layout=layout_settings(), finalize=True)

        for i in States.limiting:
            settings_window[f"{i}_include"].update(True)

        while True:
            event_settings, value_settings = settings_window.read()

            event_settings: str = event_settings

            if event_settings is None:
                settings_window.close()
                return False

            # General Settings
            elif event_settings == "language":
                settings.change_selected_lang(value_settings["language"][0:3].strip())

            elif event_settings.startswith("reset") and sg.popup_ok_cancel(trans["settings"]["conformation"]) == "OK":
                if event_settings == "reset_name":
                    reset("name")

                elif event_settings == "reset_all":
                    reset("all")

                else:
                    reset("info")

            elif event_settings == "name_key":
                for i, k in all_player():
                    main_window[f"{i} {k} frame"](value_settings[f"{i + k} name"])

            # API settings

            if event_settings == "dropie":
                change_selected_limiter(value_settings["dropie"])

            elif event_settings == "api_save":
                api = States.enable_api(value_settings["API_key"])

                if api:
                    settings_window["dropie"].update(disabled=False)
                    settings_window["activator"].update(disabled=False)

            elif event_settings == "activator" and value_settings["activator"]:
                number = 0
                include_advanced = False
                advanced_roles = []

                if value_settings["advanced_roles"]:
                    include_advanced = True
                    advanced_roles = settings.get_setting("config.json")["advanced_role"]

                for i in States.rotation[value_settings["dropie"]]:

                    if isinstance(i, str):
                        add_limiting(i, include_advanced)

                    elif isinstance(i, list):
                        for k in range(len(i)):
                            radio_key = f"{value_settings['dropie']}_{number}_{k}_radio"

                            if radio_key in value_settings and value_settings[radio_key]:
                                if len(i[k]) <= 2:
                                    for y in i[k]:
                                        add_limiting(y, include_advanced)

                                else:
                                    add_limiting(i[k], include_advanced)
                        number += 1

                main_window["role_picker"].update(values=States.limiting)

            elif event_settings == "activator" and not value_settings["activator"]:
                States.limiting = []
                main_window["role_picker"].update(role_images_finder())

            elif event_settings == "update":
                States.API.update_rotation()
                States.role_limiter()
                settings_window.close()

                return True

            elif event_settings == "theme_preview":
                if sg.popup_ok_cancel(trans["settings"]["open_theme_preview"],
                                      title=trans["settings"]["conformation"]) == "Cancel":
                    continue

                selected_theme = sg.theme_previewer(scrollable=True)
                if selected_theme:
                    settings.set_settings("config.json", setting="theme", value=selected_theme)

                    sg.popup_ok(trans["settings"]["needs_restarting"], title=trans["settings"]["info"])

            # Limiting Tab

            if event_settings.endswith("_include"):

                event_settings = event_settings.split("_")

                if len(event_settings) == 2:
                    event_settings = event_settings[0]

                    if not event_settings in States.limiting:
                        States.limiting.append(event_settings)

                    else:
                        States.limiting.remove(event_settings)

                elif len(event_settings) == 3:
                    event_settings = event_settings[0]

                    if not event_settings in States.limiting:
                        States.limiting.append(event_settings)

                        settings_window[f"{event_settings}_include"].update(True)

                    else:
                        States.limiting.remove(event_settings)

                        settings_window[f"{event_settings}_include"].update(False)

                if States.limiting:
                    main_window["role_picker"].update(States.limiting)

                else:
                    main_window["role_picker"].update(role_images_finder())


    def searcher(search_list: list[str], filter: str) -> list[str]:
        """

        :param search_list: The list to search
        :param filter: for what to search
        :return: a list that contains every item from search_list that contain the filter
        """
        final_list = []

        for i in search_list:
            if filter in i:
                final_list.append(i)

        return final_list


    while True:

        event_main, value_main = main_window.read()

        if event_main is None:
            main_window.close()
            break

        elif event_main == trans["settings"]["exit"]:
            if sg.popup_ok_cancel(trans["settings"]["conformation_leave"],
                                  title=trans["settings"]["conformation"]) == "OK":
                main_window.close()
                break

        event_main: str = event_main

        if event_main == "Info":
            info_popup()

        elif event_main == trans["settings"]["settings"]:
            while settings_win():
                settings_win()

        elif event_main == "search_bar":
            role_list = []

            if States.limiting:
                role_list = searcher(search_list=States.limiting, filter=value_main["search_bar"])

            else:
                role_list = searcher(search_list=role_images_finder(), filter=value_main["search_bar"])

            main_window["role_picker"].update(role_list)

        elif event_main[-3:] == "but":
            set_value = ""

            double_click = States.double_click(event_main)

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
                    main_window[event_main].update(image_source=image)

                    event_main = event_main.split(" ")

                    event_main: int = int(event_main[0]) + int(event_main[1])

                    States.team_dict[event_main] = set_value

                    main_window["info left"](States.info_bar())
                    set_value = ""


        elif event_main == "switcher":
            if States.current_info == "remaining":
                States.current_info = "discovered"
            else:
                States.current_info = "remaining"

            main_window["info left"](States.info_bar())


        elif event_main in [trans["settings"]["reset_name"], trans["settings"]["reset_all"],
                            trans["settings"]["reset_board"]] and sg.popup_ok_cancel(
            trans["settings"]["conformation_reset"],
            title=trans["settings"]["conformation"]) == "OK":

            if event_main == trans["settings"]["reset_name"]:
                reset("name")

            elif event_main == trans["settings"]["reset_all"]:
                reset("all")

            else:
                reset("info")
