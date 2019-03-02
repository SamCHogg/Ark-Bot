import subprocess
import argparse
import os
import tempfile
import json


def reset_mindwipes(arkprofile):
    user_id = os.path.basename(arkprofile)
    with tempfile.TemporaryDirectory() as dirpath:
        json_location = os.path.join(dirpath, '{}.json'.format(user_id))

        subprocess.run(['java', '-jar', 'ark-tools.jar', 'profileToJson', arkprofile, json_location])

        new_json = {}
        with open(json_location, 'r+') as json_file:
            data = json.loads(json_file.read())
            for profile_property in data['profile']['properties']:
                if profile_property['name'] == 'MyData':
                    for profile_data in profile_property['value']:
                        if profile_data['name'] == "MyPersistentCharacterStats":
                            for character_stats in profile_data['value']:
                                if character_stats['name'] == "CharacterStatusComponent_LastRespecAtExtraCharacterLevel":
                                    character_stats['value'] = 1
                                    new_json = data
                                    break

        with open(json_location, 'w') as json_file:
            json.dump(new_json, json_file)

        subprocess.run(['java', '-jar', 'ark-tools.jar', 'jsonToProfile', json_location, arkprofile])


def reset_user_mindwipes(steam_id, ark_install_dir):
    arkprofile = os.path.join(ark_install_dir, "{}.arkprofile".format(steam_id))
    reset_mindwipes(arkprofile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arkprofile", help="The arkprofile location")
    args = parser.parse_args()

    reset_mindwipes(args.arkprofile)
