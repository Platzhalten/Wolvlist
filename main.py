import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

def layout():
    liste = []
    for i in range(1, 17, 2):
        liste.append([sg.Frame(title=f"{i}. Player", key=f"{i}.1", layout=[[sg.Input(default_text="", key=f"{i}.2", disabled_readonly_background_color="grey", enable_events=True), sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i}.3", enable_events=True)]])])
        liste[-1].append(sg.Frame(title=f"{i + 1}. Player", key=f"{i + 1}.1", layout=[[sg.Input(default_text="", key=f"{i + 1}.2", disabled_readonly_background_color="grey", enable_events=True), sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i + 1}.3", enable_events=True)]]))

        if i in [4,8,12]:
            liste.append([sg.VSep()])

    liste.append([sg.Input(size=116)])

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
