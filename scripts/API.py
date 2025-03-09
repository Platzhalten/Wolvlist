#  Copyright (c) 2025.  Eric M.
#
#  full license at ../LICENSE
import requests
import settings


class Api:

    def __init__(self, API_key=None):
        if API_key is None:
            self.API_key = settings.get_setting("config.json", "api_key")
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

            settings.set_settings("../config.json", "api_key", self.API_key)
            settings.set_settings("../config.json", "api_key_is_valid", True)

        return req.status_code == 200


    def rotation_parser(self):

        rollen_liste = {}

        for game_mode in self.rotation:
            game_mode_name = game_mode["gameMode"]
            rollen_liste[game_mode_name] = []

            for role_rotation in game_mode["roleRotations"]:
                roles_data = role_rotation["roleRotation"]["roles"]

                for slot in roles_data:
                    roles_in_slot = []

                    for role_variant in slot:
                        if "role" in role_variant:
                            roles_in_slot.append(role_variant["role"])
                        elif "roles" in role_variant:
                            roles_in_slot.extend(role_variant["roles"])

                    if len(roles_in_slot) > 1:
                        rollen_liste[game_mode_name].append(roles_in_slot)
                    else:
                        rollen_liste[game_mode_name].append(roles_in_slot[0] if roles_in_slot else "")

        self.parsed_rotation = rollen_liste



key = Api("a very nice API key")

print(key.parsed_rotation)
