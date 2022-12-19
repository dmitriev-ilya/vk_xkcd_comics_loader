import requests


def catch_vk_api_exception(response):
    vk_api_error = response.json().get('error')
    if vk_api_error:
        error_code = vk_api_error['error_code']
        error_msg = vk_api_error['error_msg']
        error_description = f'Error {error_code}: {error_msg}'
        raise requests.HTTPError(error_description)


def get_upload_url(group_id, access_token):
    upload_server_params = {
        "group_id": group_id,
        "access_token": access_token,
        "v": 5.131,
    }
    upload_server_url = "https://api.vk.com/method/photos.getWallUploadServer"
    upload_server_response = requests.get(
        upload_server_url,
        params=upload_server_params
    )
    upload_server_response.raise_for_status()
    catch_vk_api_exception(upload_server_response)

    upload_url = upload_server_response.json()["response"]["upload_url"]
    return upload_url


def upload_image_on_vk_server(upload_url, image):
    with open(image, "rb") as file:
        files = {
            "photo": file,
        }
        upload_response = requests.post(upload_url, files=files)
    upload_response.raise_for_status()
    catch_vk_api_exception(upload_response)

    upload_params = upload_response.json()
    uploaded_photo_url = upload_params["photo"]
    upload_server_url = upload_params["server"]
    upload_hash = upload_params["hash"]
    return uploaded_photo_url, upload_server_url, upload_hash


def save_image_in_vk_group(
    group_id, access_token,
    uploaded_photo_url, upload_server_url, upload_hash
    ):
    save_method_sending = {
        "group_id": group_id,
        "photo": uploaded_photo_url,
        "server": upload_server_url,
        "hash": upload_hash,
        "access_token": access_token,
        "v": 5.131,
    }
    save_wall_method_url = "https://api.vk.com/method/photos.saveWallPhoto"
    save_wall_method_response = requests.post(
        save_wall_method_url, data=save_method_sending
    )
    save_wall_method_response.raise_for_status()
    catch_vk_api_exception(save_wall_method_response)

    save_method_params = save_wall_method_response.json()["response"][0]
    photo_owner_id = save_method_params['owner_id']
    photo_id = save_method_params['id']
    return photo_owner_id, photo_id


def publish_vk_wall_post(
    group_id, access_token,
    photo_owner_id, photo_id, text
    ):
    post_method_url = "https://api.vk.com/method/wall.post"
    post_method_params = {
        "owner_id": -group_id,
        "from_group": 1,
        "attachments": f"photo{photo_owner_id}_{photo_id}",
        "message": text,
        "access_token": access_token,
        "v": 5.131,
    }
    post_method_response = requests.get(
        post_method_url,
        params=post_method_params
    )
    post_method_response.raise_for_status()
    catch_vk_api_exception(post_method_response)
