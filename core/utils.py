import json


def open_file(path):
    with open(path) as file:
        file_content = json.load(file)
    return file_content
