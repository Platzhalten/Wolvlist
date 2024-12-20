import json
import os


def get_avaible_languages():
    check_for_lang_file()

    with open("lang.json", "r") as f:
        f = json.loads(f.read())

    liste = []

    for i in f:
        liste.append(f"{i} - {f[i]["language_full_name"]}")

    return liste

def check_for_lang_file():

    try:
        open("lang.json", "x")

    except FileExistsError:
        return True

    else:
        os.remove("lang.json")

        raise FileNotFoundError("\nNo language file was found.\nYou need one to run the Program you can find one on the Github of this Projekt https://github.com/Platzhalten/Wolvesville_list/tree/master")


get_avaible_languages()