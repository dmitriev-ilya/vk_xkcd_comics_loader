from xkdc_functions import get_xkcd_info, get_xkcd_image_name, download_xkdc_image
from vk_wall_publisher_functions import publish_vk_wall_post
import random
from environs import Env
import os


if __name__ == "__main__":
    env = Env()
    env.read_env()

    group_id = env.int("VK_GROUP_ID")
    access_token = env.str("VK_APP_ACCESS_TOKEN")
    try:
        total_xkcd = get_xkcd_info()["num"]
        comics_number = random.randint(1, total_xkcd)
        xkcd_response = get_xkcd_info(comics_number)

        image_url = xkcd_response["img"]
        image_name = get_xkcd_image_name(image_url)
        post_text = xkcd_response["alt"]
        download_xkdc_image(image_url)
    
        publish_vk_wall_post(group_id, access_token, image_name, post_text)
    finally:
        os.remove(image_name)
