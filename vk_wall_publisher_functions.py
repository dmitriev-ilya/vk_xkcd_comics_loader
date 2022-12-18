import requests


def get_upload_url(group_id, access_token):
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
    upload_url = upload_server_response.json()["response"]["upload_url"]
    return upload_url


def upload_image_on_vk_server(upload_url, image):
    with open(image, "rb") as file:
        files = {
            "photo": file,
        }
        upload_response = requests.post(upload_url, files=files)
    upload_response.raise_for_status()
    upload_info = upload_response.json()
    return upload_info


def save_image_in_vk_group(group_id, access_token, upload_info):
    save_method_data = {
        "group_id": group_id,
        "photo": upload_info["photo"],
        "server": upload_info["server"],
        "hash": upload_info["hash"],
        "access_token": access_token,
        "v": 5.131,
    }
    save_wall_method_url = "https://api.vk.com/method/photos.saveWallPhoto"
    save_wall_method_response = requests.post(
        save_wall_method_url, data=save_method_data
    )
    save_wall_method_response.raise_for_status()
    save_method_info = save_wall_method_response.json()["response"][0]
    return save_method_info


def publish_vk_wall_post(group_id, access_token, save_method_info, text):
    post_method_url = "https://api.vk.com/method/wall.post"
    post_method_params = {
        "owner_id": -group_id,
        "from_group": 1,
        "attachments": f"photo{save_method_info['owner_id']}_{save_method_info['id']}",
        "message": text,
        "access_token": access_token,
        "v": 5.131,
    }
    post_method_response = requests.get(post_method_url, params=post_method_params)
    post_method_response.raise_for_status()
