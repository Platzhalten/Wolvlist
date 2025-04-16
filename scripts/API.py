#  Copyright (c) 2025.  Eric M.
#
#  full license at ../LICENSE

import requests
from scripts import settings
class Api:

    def __init__(self, API_key=None):
        if API_key is None:
            self.API_key = settings.get_setting("config.json", "api_key")

            if self.API_key == 0 or self.API_key is None:
                raise ValueError("No API-key given in the Arguments and in the config file")

        else:
            self.API_key = API_key

        self.rotation = None
        self.parsed_rotation = None

        if self.API_key:
            self.API_key_is_valid = self.is_valid_api_key()

    def is_valid_api_key(self) -> bool:
        req = requests.request(method="Get", url="https://api.wolvesville.com/roleRotations",
                               headers={"Authorization": f"Bot {self.API_key}"})

        if req.status_code == 200:
            self.rotation = req.json()
            self.rotation_parser()

            if not settings.get_setting("config.json", "debug_mode"):
                settings.set_settings("config.json", "api_key", self.API_key)
                settings.set_settings("config.json", "api_key_is_valid", True)

        return req.status_code == 200


    def rotation_parser(self):

        if not settings.get_setting("config.json", "debug_mode") and not settings.get_setting("config.json",
                                                                                              "api_key_is_valid"):
            return False

        role_list = {}
        suffix_counter = {}

        get_role_key = lambda d: "role" if "role" in d else "roles"

        for game_mode in self.rotation:
            mode_name = game_mode["gameMode"]
            rotations = game_mode["roleRotations"]

            # Lambda-Funktion als Hilfsfunktion
            get_role_key = lambda d: "role" if "role" in d else "roles"

            for rotation in rotations:
                processed = []
                roles_data = rotation["roleRotation"]["roles"]

                for role_group in roles_data:
                    # Verarbeitung einzelner und gruppierter Rollen
                    if len(role_group) == 1:
                        processed.append(role_group[0][get_role_key(role_group[0])])
                    else:
                        group = [role[get_role_key(role)] for role in role_group]
                        processed.append(group)

                # Suffix-Logik für eindeutige Schlüssel
                clean_name = mode_name.replace("-", " ")
                suffix_counter.setdefault(clean_name, 0)
                suffix_counter[clean_name] += 1
                key = f"{clean_name} {suffix_counter[clean_name]}" if len(rotations) > 1 else clean_name

                role_list[key] = processed
        self.parsed_rotation = role_list

        settings.set_settings("config.json", "rotation", self.parsed_rotation)

        return role_list

    def update_rotation(self):

        if not settings.get_setting("config.json", "api_key_is_valid"):
            return False

        req = requests.request(method="Get", url="https://api.wolvesville.com/roleRotations",
                               headers={"Authorization": f"Bot {self.API_key}"})

        if req.status_code == 200:
            self.rotation = req.json()
            self.rotation_parser()

        else:
            return False

    def __bool__(self):
        return self.API_key_is_valid
