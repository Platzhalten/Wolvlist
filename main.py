import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

# GLOBAL VARIABEL
choosen = None

image_path = {
    "generic": {
        "evil": "images/generic/Evil.png",
        "good": "images/generic/Good.png",
        "unchecked": "images/generic/Unchecked.png",
        "unknow": "images/generic/Unknown.png"
    }
}

# OPTION

# change the order/name/add/remove theams
#       village  solo killer   unknown  ww    not Village   voting role
teams = ["gut", "solo killer", "ubk",   "ww", "kein dorf", "voting role"]
voting_roles = ["Narr", "hh", "Anarchist"]

choose_posibily = ["gut", "ubk", "evil"]

def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0 ,3):
            liste[-1].append(sg.Frame(title=f"{i + k}. Player", layout=[[sg.Button(image_source="images/generic/Unchecked.png", key=f"{i} {k} but")]]))


    liste.append([sg.Input(size=116)])
    liste.append([sg.Input(size=116, key="info out")])
    liste.append([sg.Input(size=116, key="info left")])

    adding_list = []

    for i in choose_posibily:
        adding_list.append(sg.Radio(name=i, group_id="choose", key=f"choose {i}"))

    liste.append(adding_list)

    liste.append([sg.T("Welche voting role ig: "), sg.Combo(key="narr", values=voting_roles)])

    return liste


def layout_2():
    liste = []
    for i in range(1,17):
        liste.append([sg.Input(f"{i}. Player", key=f"{i} name")])

    liste.append([sg.Button("add the names", key="name_key")])

    return liste

tab1 = sg.Tab(title="Game", layout=layout())
tab2 = sg.Tab(title="Names", layout=layout_2())

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

    
    if e[0:5] == "choose":
        for i in choose_posibily:
            if f"choose {i}" == True:
                
                choosen = i

    if e[-3:0].strip() == "but":
        pass


    if e[-1] == "3":
        number = e.split(".")

        if v[e]:
            w[f"{number[0]}.2"].update(disabled=True)
        elif not v[e]:
            w[f"{number[0]}.2"].update(disabled=False)
            
    if e[-1] == "4" or e[-1] == "3":

        aura_dict = {}
        # aura_dict = dict.fromkeys(teams, [])
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

