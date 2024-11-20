import FreeSimpleGUI as sg

sg.theme_global("DarkTeal9")

def layout():
    liste = []
    for i in range(1, 17):
        liste.append([sg.Input(default_text=f"{i}. Player", key=f"{i}.1", disabled_readonly_background_color="grey"), sg.Input(default_text="", key=f"{i}.2", disabled_readonly_background_color="grey", enable_events=True), sg.Combo(values=["alive", "dead"], default_value="alive", key=f"{i}.3", enable_events=True)])

    liste.append([sg.Input(size=102)])
    liste.append([sg.Button(button_text="Info", key="info")])

    return liste


layout = layout()

w = sg.Window(title="werville", layout=layout, icon="wolf.ico")

while True:

    e, v = w.read()

    e: str = e

    if e is None:
        w.close()
        break

    if e[-1] == "3":
        number = e.split(".")

        if v[e] == "dead":
            w[f"{number[0]}.1"].update(disabled=True)
            w[f"{number[0]}.2"].update(disabled=True)
        elif v[e] == "alive":
            w[f"{number[0]}.1"].update(disabled=False)
            w[f"{number[0]}.2"].update(disabled=False)

    if e == "info":
        liste = []

        for i in range(1, 17):
            liste.append(v[f"{i}.2"])


