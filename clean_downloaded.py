import os
import shutil

# Define the path of the file and folder
file_path = 'posts.db'
folder_path = 'downloaded'

# Check if the file exists
if os.path.exists(file_path):
    # Delete the file
    os.remove(file_path)
    print(f"{file_path} has been deleted.")
else:
    print(f"{file_path} does not exist.")

# Check if the folder exists
if os.path.exists(folder_path):
    # List the content of the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        # If it is a folder (or directory), delete it
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Folder {item_path} has been deleted.")
else:
    print(f"{folder_path} does not exist.")