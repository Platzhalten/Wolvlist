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
    reset_options = [menutrans["reset_all"], menutrans["reset_board"], menutrans["reset_name"]]

    menu_def = [[menutrans["general"],
                 [menutrans["info"], menutrans["settings"], menutrans["reset_base"], reset_options, menutrans["exit"]]]]
    liste = [[sg.MenuBar(menu_definition=menu_def)]]

    # arranging a 4x4 field for every Player and setting the Unchecked image as default
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(
                sg.Frame(title=f"{i + k}. {trans["player"]}", key=f"{i} {k} frame", element_justification="center",
                         expand_y=True, expand_x=True,
                         layout=[[sg.Button(image_source="images/generic/unchecked.png", key=f"{i} {k} but",
                                            expand_y=True, expand_x=True)],
                                 [sg.Input(key=f"{i} {k} info", size=(14, None), expand_x=True)]]))

    adding_list = []

    # Adding the radio buttons, the search bar, and arranging them into 2 rows
    for i in choose_possibility:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}", default=choose_possibility[0] == i))

    len_adding_list = int(len(adding_list) / 2) + 1
    adding_list.append(sg.Input(key="search_bar", size=26, enable_events=True))

    adding_list = [adding_list[:len_adding_list + 1], adding_list[len_adding_list + 1:]]

    # Adding the box for selecting the role
    liste.append([sg.Frame(title="", layout=adding_list, element_justification="center"),
                  sg.Listbox(values=role_images_finder(), key="role_picker", expand_x=True, expand_y=True)])

    # The remaining people bar
    liste.append([sg.Input(key="info left", default_text=get_unchecked(), expand_x=True),
                  sg.Button(button_text="⇄", key="switcher", font="ANY 6")])

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
    from main import trans, States

    set_trans = trans["settings"]

    # Name Tab
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(set_trans["change_names"], key="name_key")])

    name_layout = sg.Frame(title=set_trans["names"], layout=liste)


    # Appearance Tab
    theme_layout = sg.Frame(title="Test", layout=[[sg.Button("Open Theme Preview", key="theme_preview")]])


    language, selected = settings.get_available_languages()

    language_layout = sg.Frame(title=set_trans["language_settings"],
                               layout=[[sg.T(set_trans["language"])],
                                       [sg.Combo(key="language", values=language, default_value=selected, enable_events=True)]])

    # Api Tab
    api_key = False
    rotation = {"quick": "blabla"}

    if settings.check_for_file("config.json", leave=False):
        key = settings.get_setting("config.json", "api_key")

        if bool(key):
            api_key = key

            rotation = settings.get_setting("config.json", "rotation")

    set_api = set_trans["api"]

    api_key_layout = sg.Frame(title=set_api["api_key"],
                              layout=[[sg.Input(key="API_key"),
                                       sg.Button(set_api["api_key_safe"], key="api_save")]])

    games = list(rotation.keys())

    role_list = States.role_limiter()


    role_selection = sg.Frame(title=set_api["limit_role"],
                              layout=[[sg.DropDown(games, default_value=States.last_selected, disabled=bool(api_key) == 0, key="dropie", enable_events=True),
                                       sg.Checkbox(text=set_api["use_role_rotation"], key="activator", enable_events=True),],
                                      [sg.Checkbox(text=set_api["include_advanced"], key="advanced_roles", enable_events=True),
                                       sg.Button(button_text=set_api["update_rotation"], key="update")],
                                      role_list])

    return [
        [sg.TabGroup(layout=[[sg.Tab(title=set_trans["name_settings"], layout=[[name_layout]]),
                              sg.Tab(title=set_trans["appearance_settings"], layout=[[language_layout, theme_layout]]),
                              sg.Tab(title=set_api["api_setting"], layout=[[api_key_layout], [role_selection]],
                                     disabled=States.request_available == 0)
                              ]])]]


def info_popup() -> None:
    from main import States
    """
    Opens a popup-like window with general information about the program (e.g., version, license, source code location, and more).
    """
    layout = [[sg.T("This project is not related, supported or affiliated by Wolvesville")],
              [sg.T("This Program is licensed under the GNU GPL v3")],
              [sg.Button("Read the Full License", key="full")],
              [sg.T("The Source Code can be found on GitHub")],
              [sg.Button("Open the GitHub project", key="github")],
              [sg.T(str(States))], ]

    layout_main = sg.Tab(title="General", layout=layout)

    layout = [[sg.T("All images in the images order have been downloaded \n"
                    "via the official Wolvesville API \n\n"
                    "With the exception of the generic order \n"
                    "these come from the Wolvesville Wiki \n\n"
                    "With the exception of the random folder\n"
                    "these come from the official Google Docs\n"
                    "containing all Icons")],
              [sg.Button("Wolvesville API", key="API"),
               sg.Button("Wolvesville Wiki", key="wiki")],
              [sg.Button("Wolvesville google docs", key="doc")]]

    layout_image = sg.Tab(title="Image", layout=layout)

    if settings.check_for_file("LICENSE", do_not_ask=True):
        with open("LICENSE", "r") as f:
            license_text = f.read()

    else:
        license_text = ("No License file found\n"
                        "Please check the GitHub: https://github.com/Platzhalten/Wolvlist/blob/master/LICENSE\n"
                        "or the GNU GPL 3.0 license: https://www.gnu.org/licenses/gpl-3.0.de.html")

    layout = [[sg.Multiline(license_text, disabled=True, expand_x=True, expand_y=True)],]

    layout_license = sg.Tab(title="License", layout=layout)

    tab = sg.TabGroup(layout=[[layout_main], [layout_image], [layout_license]], expand_x=True, expand_y=True, key="tab")

    w1 = sg.Window(title="Info", layout=[[tab], [sg.Button("close", key="close")]], keep_on_top=True, resizable=True, finalize=True)
    w1.set_min_size(w1.size)


    while True:
        event_popup, v = w1.read()

        if event_popup is None or event_popup == "close":
            w1.close()
            break

        elif event_popup == "full":
            if license_text.startswith("No License"):
                wb.open(url="https://www.gnu.org/licenses/gpl-3.0")

            else:
                w1["tab"].Widget.select(2)

        elif event_popup == "github":
            wb.open(url="https://github.com/Platzhalten/Wolvlist")

        elif event_popup == "API":
            wb.open(url="https://api-docs.wolvesville.com/#/")

        elif event_popup == "wiki":
            wb.open(url="https://wolvesville.fandom.com/wiki/Wolvesville_Wiki")

        elif event_popup == "doc":
            wb.open(url="https://drive.google.com/drive/folders/1Ou_1hbC_3GF2n4qjxY9hLWUvApC_w6BF")
