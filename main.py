import os
import random

from environs import Env

from vk_wall_publisher_functions import get_upload_url
from vk_wall_publisher_functions import publish_vk_wall_post
from vk_wall_publisher_functions import save_image_in_vk_group
from vk_wall_publisher_functions import upload_image_on_vk_server
from xkdc_functions import download_xkdc_image
from xkdc_functions import get_xkcd_comics
from xkdc_functions import get_xkcd_image_name


if __name__ == "__main__":
    env = Env()
    env.read_env()
    group_id = env.int("VK_GROUP_ID")
    access_token = env.str("VK_APP_ACCESS_TOKEN")

    try:
        total_xkcd = get_xkcd_comics()["num"]
        comics_number = random.randint(1, total_xkcd)
        xkcd_comics = get_xkcd_comics(comics_number)

        image_url = xkcd_comics["img"]
        image_name = get_xkcd_image_name(image_url)
        post_text = xkcd_comics["alt"]
        download_xkdc_image(image_url)

        upload_url = get_upload_url(group_id, access_token)

        (uploaded_photo_url,
        upload_server_url,
        upload_hash) = upload_image_on_vk_server(upload_url, image_name)

        photo_owner_id, photo_id = save_image_in_vk_group(
            group_id,
            access_token,
            uploaded_photo_url,
            upload_server_url,
            upload_hash
        )

        publish_vk_wall_post(
            group_id,
            access_token,
            photo_owner_id,
            photo_id,
            post_text
        )
    finally:
        os.remove(image_name)
