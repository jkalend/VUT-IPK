import os


def find_file(filename, search_path):
    for root, dir, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)

