import os
import requests
 
IG_BUISNESS_ACCOUNT_ID = "17841478078172531"
ACCESS_TOKEN = "EAAVvM9MLeuABPxT3XIVuMmNLrcY5SBat27uBOF73HZCi27DiHlPV8YaqNgZCT44z6bPynnlV2ZCpFs03bCDpuNFOGRkLgJ78cB8nBXbQQhD7lZBrcrx6ovR7K8Ke7uWDMSxxZCPAo2SNZAyyvntyJRAQYw0ZA2ZCxIyOVbZBH8tMXrL7ZB0aCZAZCIPZC3IphUQZBbCFThjzhJf4IaZBrOof1E9orPTv5tZC5sVT9Au1JA9pr6kpYtkZD"
IMAGE_URL = "https://i.imgur.com/b1QKyXN.jpeg"
CAPTION = "Hello world!"


# --- API Details ---
API_VERSION = "v24.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
ENDPOINT = f"/{IG_BUSINESS_ACCOUNT_ID}/media"

def send_post():







URL = BASE_URL + ENDPOINT

# --- Payload ---
# The -F flags in curl translate to the 'data' or 'files' parameter in requests. 
# For simple key/value pairs like this, 'data' is sufficient.
payload = {
    "image_url": IMAGE_URL,
    "caption": CAPTION,
    "access_token": ACCESS_TOKEN
}

# --- Make the POST Request ---
try:
    response = requests.post(URL, data=payload)
    
    # Raise an exception for bad status codes (4xx or 5xx)
    response.raise_for_status() 

    # Parse the JSON response
    data = response.json()

    print("✅ Request Successful!")
    print(f"Status Code: {response.status_code}")
    
    # The response will contain the Media Creation ID
    print(f"Response (Media Creation ID): {data.get('id')}")

    # Note: This only creates the media container. You'll need a second request 
    # to the /media_publish endpoint using this 'id' to actually post it.

except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred: {e}")
    if 'response' in locals():
        print(f"Error Response: {response.text}")
