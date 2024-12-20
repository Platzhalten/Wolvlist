import json
import os


def get_avaible_languages():
    check_for_lang_file()

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    liste = []

    for i in f:
        if not i == "selected":

            liste.append(f"{i} - {f[i]["language_full_name"]}")

    return [liste[1:], f["selected"]]


def get_settings(language: str = None) -> dict:

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    if language is None:
        language = f["selected"]

    return f[language[0:2]]


def change_selected_lang(lang: str):

    with open("lang.json", "r") as f:

        l = json.loads(f.read())

        l["selected"] = lang

        print(l)

    with open("lang.json", "w") as f:
        print(json.dumps(l))
        f.write(json.dumps(l, indent=3))

def check_for_lang_file():
    try:
        open("lang.json", "x")

    except FileExistsError:
        return True

    else:
        os.remove("lang.json")

        raise FileNotFoundError("\nNo language file was found.\nYou need one to run the Program you can find one on the Github of this Projekt https://github.com/Platzhalten/Wolvesville_list/tree/master")
