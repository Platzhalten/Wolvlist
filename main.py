import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

# OPTION

# change the order/name/add/remove theams
#       village  solo killer   unknown  ww    not Village   voting role
teams = ["gut", "solo killer", "ubk",   "ww", "kein dorf", "voting role"]
voting_roles = ["Narr", "hh", "Anarchist"]

def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([])

        for k in range(0 ,3):
            liste[-1].append(sg.Frame(title=f"{i + k}. Player", layout=[[sg.Button(image_source="images/generic/Good.png", size=(5,5))]]))


        # liste.append([sg.Frame(title=f"{i}. Player", key=f"{i}.1", layout=[[sg.Input(default_text="", key=f"{i}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Checkbox(text="Dead" , key=f"{i}.3", enable_events=True), sg.Combo(values=teams, key=f"{i}.4", enable_events=True)]])])
        # liste[-1].append(sg.Frame(title=f"{i + 1}. Player", key=f"{i + 1}.1", layout=[[sg.Input(default_text="", key=f"{i + 1}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Checkbox(text="Dead" , key=f"{i + 1}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 1}.4", enable_events=True)]]))
        # liste[-1].append(sg.Frame(title=f"{i + 2}. Player", key=f"{i + 2}.1", layout=[[sg.Input(default_text="", key=f"{i + 2}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Checkbox(text="Dead" , key=f"{i + 2}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 2}.4", enable_events=True)]]))
        # liste[-1].append(sg.Frame(title=f"{i + 3}. Player", key=f"{i + 3}.1", layout=[[sg.Input(default_text="", key=f"{i + 3}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Checkbox(text="Dead" , key=f"{i + 3}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 3}.4", enable_events=True)]]))

    liste.append([sg.Input(size=116)])
    liste.append([sg.Input(size=116, key="info out")])
    liste.append([sg.Input(size=116, key="info left")])
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

