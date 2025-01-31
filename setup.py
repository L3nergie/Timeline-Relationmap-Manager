import os
import json

def create_directories_and_files():
    project_dir = '/Users/ericmurray/development/fortuna_island/app/timeline-relationmap'
    data_dir = os.path.join(project_dir, 'data')
    json_dir = os.path.join(data_dir, 'json')
    json_file_path = os.path.join(json_dir, 'project_directories.json')

    # Créer les répertoires si ils n'existent pas
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    # Créer le fichier JSON si il n'existe pas
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as file:
            json.dump({}, file, indent=4)

if __name__ == "__main__":
    create_directories_and_files()
