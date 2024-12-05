import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

# GLOBAL VARIABEL
choosen = None

image_path = {
    "generic": {
        "böse": "images/generic/Evil.png",
        "gut": "images/generic/Good.png",
        "unchecked": "images/generic/Unchecked.png",
        "ubk": "images/generic/Unknown.png"
    },

    "voting": {
        "generic": "images/voting/Generic.png",
        "anarchist": "images/voting/Anarchist.png",
        "fool": "images/voting/Fool.png",
        "hh": "images/voting/Headhunter.png"
    }
}

# OPTION

# change the order/name/add/remove theams
#       village  solo killer   unknown  ww    not Village   voting role
teams = ["gut", "solo killer", "ubk",   "ww", "kein dorf", "voting role"]
voting_roles = ["Narr", "hh", "Anarchist"]

choose_posibily = ["gut", "ubk", "böse", "Narr/HH", "unchecked"]


def get_image_path(image: str, type: str = "generic"):

    return image_path[type][image]


def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0, 4):
            liste[-1].append(sg.Frame(title=f"{i + k}. Player", size=(125, 125), layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but", metadata="Unchecked")]]))

    # liste.append([sg.Radio(text="Good", group_id="choose", key="choose Good"), sg.Radio(text="ubk", group_id="choose"), sg.Radio(text="evil", group_id="choose"), sg.Radio(text="unchecked", group_id="choose")])

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

            wert1 = "generic"

            if set_value == "Narr/HH":
                wert1 = "voting"
                set_value="generic"

            w[e].update(image_source=get_image_path(image=set_value, type=wert1))
            set_value = ""

"""
        aura_dict = {}
        for i in teams:
            aura_dict[i] = []

        player_list = range(1,17)

        no_info = []

        for i in range(1, 17):
            wert = v[f"{i}.4"]

            if wert:
                aura_dict[wert].append(i)
            elif not wert and v[f"{i}.3"] == False:
                no_info.append(str(i) + " ")

        info_list = []

        if no_info:
            w["info left"]("".join(no_info) + "übrig")
        else:
            w["info left"]("Alle wurden überprüft")

        for i in aura_dict:
            temp_list = []

            for k in aura_dict[i]:
                if v[f"{k}.3"] == "alive":

                    if not temp_list == []:
                        temp_list.append(", ")

                    temp_list.append(str(k))

            if not temp_list == []:
                temp_list.append(" " + i + " | ")

            info_list.append("".join(temp_list))

        info = "".join(info_list).removesuffix(" | ")

        if v["narr"]:
            info = info.replace("voting role", v["narr"])

        w["info out"](info)

"""