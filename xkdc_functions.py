import requests
from urllib.parse import urlparse, unquote
import os
import argparse


def get_xkcd_info(comics_num=None):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Скрипт скачивает комикс с сайта https://xkcd.com"""
    )
    parser.add_argument(
        "-c",
        "--comics_num",
        help="номер комикса, по умолчанию - последний",
        default=None,
    )
    args = parser.parse_args()

    image_url = get_xkcd_info(args.comics_num)["img"]
    download_xkdc_image(image_url)
