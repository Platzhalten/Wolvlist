import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

# OPTION

# change the order/name/add/remove theams
#       village  solo    ww    unknown  not Village
teams = ["gut", "solo", "ww", "ubk", "kein dorf"]


def layout():
    liste = []
    for i in range(1, 17, 4):
        liste.append([sg.Frame(title=f"{i}. Player", key=f"{i}.1", layout=[[sg.Input(default_text="", key=f"{i}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i}.3", enable_events=True), sg.Combo(values=teams, key=f"{i}.4", enable_events=True)]])])
        liste[-1].append(sg.Frame(title=f"{i + 1}. Player", key=f"{i + 1}.1", layout=[[sg.Input(default_text="", key=f"{i + 1}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i + 1}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 1}.4", enable_events=True)]]))
        liste[-1].append(sg.Frame(title=f"{i + 2}. Player", key=f"{i + 2}.1", layout=[[sg.Input(default_text="", key=f"{i + 2}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i + 2}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 2}.4", enable_events=True)]]))
        liste[-1].append(sg.Frame(title=f"{i + 3}. Player", key=f"{i + 3}.1", layout=[[sg.Input(default_text="", key=f"{i + 3}.2", disabled_readonly_background_color="grey", enable_events=True, size=20)], [sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i + 3}.3", enable_events=True), sg.Combo(values=teams, key=f"{i + 3}.4", enable_events=True)]]))

    liste.append([sg.Input(size=116)])
    liste.append([sg.Input(size=116, key="info out")])
    liste.append([sg.Input(size=116, key="info left")])

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

w = sg.Window(title="werville", layout=tab)

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

        if v[e] == "dead":
            w[f"{number[0]}.2"].update(disabled=True)
        elif v[e] == "alive":
            w[f"{number[0]}.2"].update(disabled=False)
            
    if e[-1] == "4" or e[-1] == "3":

        aura_dict = {}
        # aura_dict = dict.fromkeys(teams, [])
        for i in teams:
            aura_dict[i] = []

        player_list = range(1,17)

        for i in range(1, 17):
            wert = v[f"{i}.4"]

            if wert:
                aura_dict[wert].append(i)

        info_list = []

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

        w["info out"](info)

