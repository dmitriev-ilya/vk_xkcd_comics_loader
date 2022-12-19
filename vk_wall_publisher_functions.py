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
    upload_params = upload_response.json()
    return upload_params


def save_image_in_vk_group(group_id, access_token, upload_params):
    save_method_sending = {
        "group_id": group_id,
        "photo": upload_params["photo"],
        "server": upload_params["server"],
        "hash": upload_params["hash"],
        "access_token": access_token,
        "v": 5.131,
    }
    save_wall_method_url = "https://api.vk.com/method/photos.saveWallPhoto"
    save_wall_method_response = requests.post(
        save_wall_method_url, data=save_method_sending
    )
    save_wall_method_response.raise_for_status()
    save_method_params = save_wall_method_response.json()["response"][0]
    return save_method_params


def publish_vk_wall_post(group_id, access_token, save_method_params, text):
    post_method_url = "https://api.vk.com/method/wall.post"
    post_method_params = {
        "owner_id": -group_id,
        "from_group": 1,
        "attachments": f"photo{save_method_params['owner_id']}_{save_method_params['id']}",
        "message": text,
        "access_token": access_token,
        "v": 5.131,
    }
    post_method_response = requests.get(post_method_url, params=post_method_params)
    post_method_response.raise_for_status()
