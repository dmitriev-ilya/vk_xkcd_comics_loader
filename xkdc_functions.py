import os
from urllib.parse import unquote
from urllib.parse import urlparse

import requests


def get_xkcd_comics(comics_num=None):
    comics_url = "https://xkcd.com/info.0.json"
    if comics_num:
        comics_url = f"https://xkcd.com/{comics_num}/info.0.json"
    xkcd_response = requests.get(comics_url)
    xkcd_response.raise_for_status()
    return xkcd_response.json()


def get_xkcd_image_name(image_url):
    path = unquote(urlparse(image_url).path)
    return os.path.split(path)[1]


def download_xkdc_image(image_url):
    image_name = get_xkcd_image_name(image_url)
    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_name, "wb") as file:
        file.write(response.content)
