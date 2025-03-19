import os
import shutil

def move_unneeded_files(directory, target_folder="Delete"):
    # Create the target folder if it doesn't exist
    target_path = os.path.join(directory, target_folder)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") or file.endswith(".pyc"):
                if file not in [
                    "main.py",
                    "snipester_utils.py",
                    "snipester_refresh.py",
                    "snipester_update_refresh.py",
                    "snipester_auction_ended.py",
                    "globals.py",
                    "http_engine.py",
                    "data_extraction.py",
                ]:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(target_path, file)
                    shutil.move(old_path, new_path)
                    print(f"Moved: {old_path} -> {new_path}")

# Specify the directory to scan
directory = r"d:\drevo\OneDrive\Documents\.Documents\repos\snipester"
move_unneeded_files(directory)
