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

        return req.status_code == 200

    def rotation_parser(self):
        if self.rotation is None:
            return False

        print(self.rotation)
        print(self.rotation[0]["roleRotations"])

        f = self.rotation[0]["roleRotations"]["roles"]

        role_list = []

        for i in f:
            if len(i) >= 2:
                role_list.append([])
                for k in i:
                    role_list[-1].append(k["role"].replace("-", " "))

            else:
                role_list.append(i[0]["role"].replace("-", " "))

        self.parsed_rotation = role_list

        return self.parsed_rotation


key = Api("a very nice API key")

print(key.parsed_rotation)

test = [{'roleRotation':
             {'id': '2a6690ec-4843-4223-bbc4-d42fd0d7ac54', 'roles':
                 [[{'probability': 1.0, 'role': 'aura-seer'}],
                  [{'probability': 1.0, 'role': 'medium'}],
                  [{'probability': 1.0, 'role': 'jailer'}],
                  [{'probability': 0.5, 'role': 'party-wolf'}, {'probability': 0.5, 'role': 'junior-werewolf'}],
                  [{'probability': 1.0, 'role': 'doctor'}],
                  [{'probability': 1.0, 'role': 'alpha-werewolf'}],
                  [{'probability': 1.0, 'role': 'detective'}],
                  [{'probability': 0.5, 'role': 'fool'}, {'probability': 0.5, 'role': 'headhunter'}],
                  [{'probability': 1.0, 'role': 'bodyguard'}],
                  [{'probability': 1.0, 'role': 'witch'}],
                  [{'probability': 1.0, 'role': 'shadow-wolf'}],
                  [{'probability': 1.0, 'role': 'cursed-human'}],
                  [{'probability': 0.5, 'role': 'corruptor'}, {'probability': 0.5, 'role': 'bandit'}],
                  [{'probability': 1.0, 'role': 'mayor'}], [{'probability': 1.0, 'role': 'wolf-seer'}],
                  [{'probability': 1.0, 'role': 'loudmouth'}]]}, 'probability': 1.0}]
