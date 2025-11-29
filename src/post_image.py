import requests
import time

# Your values here
access_token = "EAAMgKdh8ZCJsBP3ktyJqS5C04FaYxQGzsq46A6iCfYI8nBrvf3JXA6hKhbW3waW023TxdipZAbLISLPRewMdgjTnpCowGAfwtvLun3giXAGBQZAzfQ4oEX7ZBo2TH4qOpBDmta2fJIJj0JicyBZCLkYMhxraV7ltRMvW4bPoTVqy8c95xksxpjhRziZBZBY"
instagram_user_id = "17841478078172531"  # e.g. "1784140..."
image_url = "https://yourdomain.com/path/to/image.jpg"  # must be public
caption = "Here is my caption for the Instagram post!"

# 1) Create a media container
create_url = f"https://graph.facebook.com/v16.0/{instagram_user_id}/media"
create_payload = {
    "image_url": image_url,
    "caption": caption,
    "access_token": access_token
}

res = requests.post(create_url, data=create_payload)
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

res2 = requests.post(publish_url, data=publish_payload)
res2.raise_for_status()
publish_data = res2.json()
print("Publish response:", publish_data)

