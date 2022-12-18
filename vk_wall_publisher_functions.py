import requests
from environs import Env
import argparse


def publish_vk_wall_post(group_id, access_token, image, text):
    upload_server_params = {
        "group_id": group_id,
        "access_token": access_token,
        "v": 5.131,
    }
    upload_server_url = "https://api.vk.com/method/photos.getWallUploadServer"
    upload_server_response = requests.get(
        upload_server_url, params=upload_server_params
    )
    upload_server_response.raise_for_status()
    with open(image, "rb") as file:
        upload_url = upload_server_response.json()["response"]["upload_url"]
        files = {
            "photo": file,
        }
        upload_response = requests.post(upload_url, files=files)
    upload_response.raise_for_status()
    upload_response = upload_response.json()

    save_wall_method_data = {
        "group_id": group_id,
        "photo": upload_response["photo"],
        "server": upload_response["server"],
        "hash": upload_response["hash"],
        "access_token": access_token,
        "v": 5.131,
    }
    save_wall_method_url = "https://api.vk.com/method/photos.saveWallPhoto"
    save_wall_method_response = requests.post(
        save_wall_method_url, data=save_wall_method_data
    )
    save_wall_method_response.raise_for_status()
    save_wall_method_response = save_wall_method_response.json()["response"][0]

    post_method_url = "https://api.vk.com/method/wall.post"
    post_method_params = {
        "owner_id": -group_id,
        "from_group": 1,
        "attachments": f"photo{save_wall_method_response['owner_id']}_{save_wall_method_response['id']}",
        "message": text,
        "access_token": access_token,
        "v": 5.131,
    }
    post_method_response = requests.get(post_method_url, params=post_method_params)
    post_method_response.raise_for_status()
