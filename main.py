from xkdc_functions import get_xkcd_info, get_xkcd_image_name, download_xkdc_image
from vk_wall_publisher_functions import (
    get_upload_url,
    upload_image_on_vk_server,
    save_image_in_vk_group,
    publish_vk_wall_post,
)
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
        xkcd_info = get_xkcd_info(comics_number)

        image_url = xkcd_info["img"]
        image_name = get_xkcd_image_name(image_url)
        post_text = xkcd_info["alt"]
        download_xkdc_image(image_url)

        upload_url = get_upload_url(group_id, access_token)
        upload_info = upload_image_on_vk_server(upload_url, image_name)
        save_method_info = save_image_in_vk_group(group_id, access_token, upload_info)
        publish_vk_wall_post(group_id, access_token, save_method_info, post_text)
    finally:
        os.remove(image_name)
