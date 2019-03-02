import subprocess
import argparse
import os
import tempfile
import json
import shutil
import time

parser = argparse.ArgumentParser()
parser.add_argument("arkprofile", help="The arkprofile location")
args = parser.parse_args()

user_id = os.path.basename(args.arkprofile)

backup_dir = '/home/sam/ARK-Engram-Remover/backups/'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
shutil.copyfile(args.arkprofile, '{}{}.backup-{}'.format(backup_dir, user_id, int(time.time())))


with tempfile.TemporaryDirectory() as dirpath:
    json_location = os.path.join(dirpath, '{}.json'.format(user_id))

    subprocess.run(['java', '-jar', 'ark-tools.jar', 'profileToJson', args.arkprofile, json_location])

    new_json = {}
    with open(json_location, 'r+') as json_file:
        data = json.loads(json_file.read())
        for profile_property in data['profile']['properties']:
            if profile_property['name'] == 'MyData':
                for profile_data in profile_property['value']:
                    if profile_data['name'] == "MyPersistentCharacterStats":
                        for character_stats in profile_data['value']:
                            if character_stats['name'] == "PlayerState_EngramBlueprints":
                                character_stats['value'] = []
                                new_json = data
                                break

    with open(json_location, 'w') as json_file:
        json.dump(new_json, json_file)

    subprocess.run(['java', '-jar', 'ark-tools.jar', 'jsonToProfile', json_location, args.arkprofile])
