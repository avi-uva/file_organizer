import os 
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("Starting script...")  # Debugging start point

source_dir = "/Users/aviuvaydov/downloads"
dest_dir_jpgs = "/Users/aviuvaydov/Downloads/Downloaded jpeg_jpg"

# Ensure the destination directory exists only once at the start
if not os.path.exists(dest_dir_jpgs):
    os.makedirs(dest_dir_jpgs)
    print(f"Created directory: {dest_dir_jpgs}")  # Debugging line

print("Path assigned successfully...")  # Debugging checkpoint

def make_unique(destination, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    # IF FILE EXISTS, ADD NUMBER TO THE END OF THE FILENAME
    while os.path.exists(os.path.join(destination, name)):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move(destination, entry, name):  # Moves file to destination folder
    # Check if the destination path is a directory and create it if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)  # Ensure the folder is there but only if it doesn't exist already
        print(f"Created destination directory: {destination}")

    # Check if the file already exists in the destination
    file_exists = os.path.exists(os.path.join(destination, name))
    if file_exists:
        unique_name = make_unique(destination, name)
        shutil.move(entry.path, os.path.join(destination, unique_name))  # Correctly build the full path
    else:
        shutil.move(entry.path, os.path.join(destination, name))  # Correctly build the full path

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Modification detected...")  # Debugging line
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():  # Only move files, not directories
                    name = entry.name
                    print(f"Detected file: {name}")  # Debugging line
                    destination = dest_dir_jpgs
                    if name.endswith('.jpg') or name.endswith('.jpeg'):
                        print(f"Moving {name} to {destination}")  # Debugging line
                        move(destination, entry, name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
