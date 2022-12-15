import requests
from urllib.parse import urlparse
from main_loader_functions import load_picture
import argparse


def get_xkcd_response(comics_num=None):
    comics_url = "https://xkcd.com/info.0.json"
    if comics_num:
        comics_url = f"https://xkcd.com/{comics_num}/info.0.json"
    xkcd_response = requests.get(comics_url)
    xkcd_response.raise_for_status()
    return xkcd_response.json()


def get_xkcd_image_name(image_url):
    path = urlparse(image_url).path
    return path.split("/")[-1]


def load_xkdc_image(image_url):
    image_name = get_xkcd_image_name(image_url)
    load_picture(image_url, image_name)


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

    image_url = get_xkcd_response(args.comics_num)["img"]
    load_xkdc_image(image_url)
