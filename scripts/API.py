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

        for game_mode in self.rotation:
            game_mode_name = game_mode['gameMode']
            role_rotations = game_mode['roleRotations']
            num_rotations = len(role_rotations)

            if num_rotations == 1:
                role_rotation = role_rotations[0]
                roles_data = role_rotation['roleRotation']['roles']
                processed_roles = []
                for role_group in roles_data:
                    if len(role_group) == 1:
                        role_dict = role_group[0]
                        if 'role' in role_dict:
                            processed_roles.append(role_dict['role'])
                        elif 'roles' in role_dict:
                            processed_roles.append(role_dict['roles'])
                    else:
                        sublist = []
                        for role_dict in role_group:
                            if 'role' in role_dict:
                                sublist.append([role_dict['role']])
                            elif 'roles' in role_dict:
                                sublist.append(role_dict['roles'])
                        processed_roles.append(sublist)
                role_list[game_mode_name] = processed_roles
            else:
                used_suffixes = []
                for role_rotation in role_rotations:
                    roles_data = role_rotation['roleRotation']['roles']
                    processed_roles = []
                    for role_group in roles_data:
                        if len(role_group) == 1:
                            role_dict = role_group[0]
                            if 'role' in role_dict:
                                processed_roles.append(role_dict['role'])
                            elif 'roles' in role_dict:
                                processed_roles.append(role_dict['roles'])
                        else:
                            sublist = []
                            for role_dict in role_group:
                                if 'role' in role_dict:
                                    sublist.append([role_dict['role']])
                                elif 'roles' in role_dict:
                                    sublist.append(role_dict['roles'])
                            processed_roles.append(sublist)

                    used_suffixes.append(game_mode)
                    suffex = used_suffixes.count(game_mode)

                    role_list[f"{game_mode_name.replace("-", " ")} {suffex}"] = processed_roles

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
