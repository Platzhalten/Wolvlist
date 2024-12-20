import FreeSimpleGUI as sg
import settings

sg.theme_global("DarkGrey11")


# GLOBAL VARIABEL
choosen = None

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
choose_posibily = [team["good"], team["unknown"] , team["evil"], team["voting_role"], team["unchecked"], team["dead"]]

team_dict = dict.fromkeys(range(1,17), team["unchecked"])


def get_image_path(image: str):
    return image_path[image]


def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(sg.Frame(title=f"{i + k}. {trans["player"]}", size=(125, 125), layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")]]))

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(text=i, group_id="choose", key=f"choose {i}"))

    liste.append(adding_list)


    liste.append([sg.Input(size=116)])
    liste.append([sg.Input(size=116, key="info out")])
    liste.append([sg.Input(size=116, key="info left")])

    return liste


def layout_settings():
    name_layout = []
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. {trans["player"]}", key=f"{i} name")])

    liste.append([sg.Button(trans["settings"]["change_names"], key="name_key")])

    name_layout.append(sg.Frame(title=trans["settings"]["names"], layout=liste))

    languafe = settings.get_avaible_languages()

    game_layout = [[sg.T("Language (needs restarting)")],
                   [sg.Combo(key="lang", values=languafe[0], default_value=languafe[1], enable_events=True)],
                   [sg.T(trans["what_voting_role"])],
                   [sg.Combo(key="narr", values=voting_roles)]]

    game_layout = [sg.Frame(title=trans["settings"]["games_settings"], layout=game_layout)]


    return [name_layout, game_layout]

tab1 = sg.Tab(title="Game", layout=layout())
tab2 = sg.Tab(title="Settings", layout=layout_settings())


tab = [[sg.TabGroup(layout=[[tab1, tab2]])]]

w = sg.Window(title="werville", layout=tab, resizable=True)

while True:

    e, v = w.read()

    e: str = e

    print(e)

    if e is None:
        w.close()
        break

    elif e == "name_key":
        for i in range(1,17):

            w[f"{i}.1"](v[f"{i} name"])


    elif e[-3:] == "but":
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

    elif e == "lang":
        settings.change_selected_lang(v["lang"][0:3].strip())