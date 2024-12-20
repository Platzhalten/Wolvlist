import FreeSimpleGUI as sg
import settings

sg.theme_global("DarkGrey11")


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
            liste[-1].append(sg.Frame(title=f"{i + k}. Player", size=(125, 125), layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")]]))

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
        liste.append([sg.Input(f"{i}. Player", key=f"{i} name")])

    liste.append([sg.Button("add the names", key="name_key")])

    name_layout.append(sg.Frame(title="Names", layout=liste))


    game_layout = [[sg.T("What Language?")],
                   [sg.Combo(key="lang", values=settings.get_avaible_languages())],
                   [sg.T("Welche Voting Roles gibt es")],
                   [sg.Combo(key="narr", values=voting_roles)]]

    game_layout = [sg.Frame(title="Game Settings", layout=game_layout)]


    return [name_layout, game_layout]


def get_extra_info():
    pass


tab1 = sg.Tab(title="Game", layout=layout())
tab2 = sg.Tab(title="Settings", layout=layout_settings())


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
            if v["narr"] == set_value == "Narr/HH":
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
