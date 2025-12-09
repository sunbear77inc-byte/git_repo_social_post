import requests
import time

# Your values here
access_token = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY"
instagram_user_id = "17841478078172531"  # e.g. "1784140..."
image_url = "https://yourdomain.com/path/to/image.jpg"  # must be public
caption = "Here is my caption for the Instagram post!"


# --- ADD THIS HEADER DICTIONARY ---
custom_headers = {
    # This header makes the request look like it's from Safari on a recent iPhone
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1'
}
# -----------------------------------



# 1) Create a media container
create_url = f"https://graph.facebook.com/v16.0/{instagram_user_id}/media"
create_payload = {
    "image_url": image_url,
    "caption": caption,
    "access_token": access_token
}

res = requests.post(create_url, data=create_payload, headers=custom_headers)
res.raise_for_status()
create_data = res.json()
print("Create response:", create_data)

if "id" not in create_data:
    raise Exception("No creation ID returned by Instagram API")

creation_id = create_data["id"]

# 2) Publish the media container
publish_url = f"https://graph.facebook.com/v16.0/{instagram_user_id}/media_publish"
publish_payload = {
    "creation_id": creation_id,
    "access_token": access_token
}

# Sometimes you need to wait a little (depending on crawl)
time.sleep(5)  # wait 5 seconds — adjust if needed

res2 = requests.post(publish_url, data=publish_payload, headers=custom_headers)
res2.raise_for_status()
publish_data = res2.json()
print("Publish response:", publish_data)

