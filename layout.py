import FreeSimpleGUI as sg

import settings


def entire_layout():
    tab1 = sg.Tab(title="Game", layout=layout())
    tab2 = sg.Tab(title="Settings", layout=layout_settings())

    tab = [[sg.TabGroup(layout=[[tab1, tab2]])]]

    return tab


def layout():
    from main import trans, choose_posibily

    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(sg.Frame(title=f"{i + k}. {trans["player"]}", key=f"{i} {k} frame", size=(125, 125), layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but", bind_return_key='<Double-1>')]]))

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}"))

    liste.append(adding_list)

    liste.append([sg.Input(size=75, key="info out")])
    liste.append([sg.Input(size=75, key="info left", default_text=f"{str(list(range(1, 17))).replace("[", "").replace("]", "").replace(",", "")} übrig")])

    return liste


def layout_settings():
    from main import trans, voting_roles

    name_layout = []
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(trans["settings"]["change_names"], key="name_key")])

    name_layout = sg.Frame(title=trans["settings"]["names"], layout=liste)

    languafe = settings.get_avaible_languages()

    game_layout = [[sg.T("Language (needs restarting)")],
                   [sg.Combo(key="lang", values=languafe[0], default_value=languafe[1], enable_events=True)],
                   [sg.T(trans["what_voting_role"])],
                   [sg.Combo(key="narr", values=voting_roles)]]

    game_layout = sg.Frame(title=trans["settings"]["games_settings"], layout=game_layout)


    return [[name_layout], [game_layout]]

