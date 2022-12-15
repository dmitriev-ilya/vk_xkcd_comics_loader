from os.path import splitext
from urllib.parse import urlparse

import requests


def load_picture(url, filename, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(response.content)


def get_extension(url):
    path = urlparse(url).path
    file_path, extension = splitext(path)
    return extension
