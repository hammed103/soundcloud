import pandas as pd
import requests
from datetime import datetime
import base64
from bs4 import BeautifulSoup

# List of client IDs and client secrets
client_ids = ["53fb1dbe5f42480ba654fcc3c7e168d6", "cb7eb4ee66a543dab0c56e3e8db63475", "20f25a5cbcb84d998d91ec0e29529b0e","ab3f711fb94e43c29f107504e2bc6c2e","39381b8f10524649a65923eb264f55c1","f7c3b2637f704afeb838c3a9ebbfa03e"]
client_secrets = ["5c1da4cce90f410e88966cdfc0785e3a", "2d5ea5e9d05945ec92bcf0bbe837c573", "f773eee78b76468098da352c669228d8","3ac0d4cc5622440ca60a1dee3c0c1e9f","56f690af59db4b53a6fa3ebb0b5398fa","f7c3b2637f704afeb838c3a9ebbfa03e"]

import json
import os
from django.conf import settings
# Set your client key and secret

#json_file_path =  r"C:\Users\SteelSeries\Desktop\Upwork\Alex M\cloud\top50chart\back\charts\statiic\grouped_data.json"
static_folder = settings.STATIC_ROOT
json_file_path = os.path.join(static_folder, "grouped_data.json")

# Read the JSON file and convert it into a dictionary
with open(json_file_path, 'r') as json_file:
    loaded_data = json.load(json_file)


def create_soup_from_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None





def get_access_token(client_id,client_secret):
    url = "https://accounts.spotify.com/api/token"

    # Encode the client_id and client_secret using base64
    credentials = f"{client_id}:{client_secret}"
    credentials_bytes = credentials.encode("ascii")
    credentials_base64 = base64.b64encode(credentials_bytes).decode("ascii")

    headers = {"Authorization": "Basic " + credentials_base64}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        # Use the access_token for your API requests
        print(f"Access Token: {access_token}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return access_token


# Initialize the Spotify client
access_token = get_access_token(client_ids[0], client_secrets[0])

def search_spotify_albums(query, client_ids, client_secrets, max_attempts=6):
    global access_token
    for attempt in range(max_attempts):
        if attempt > 0:
            client_id = client_ids[(attempt - 1) % len(client_ids)]
            client_secret = client_secrets[(attempt - 1) % len(client_secrets)]
            access_token = get_access_token(client_id, client_secret)

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        url = f"https://api.spotify.com/v1/search"
        params = {
            "q": query,
            "type": "track",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            search_results = response.json()
            return search_results
        else:
            print(f"Attempt {attempt + 1}: Request failed with status code {response.status_code}")
            
            if attempt < max_attempts - 1:
                print("Retrying...")
            else:
                print("Max attempts reached. Giving up.")
                return None


import re
def book(track_name,tag,url):
  global loaded_data
  try:
    result = list(loaded_data[url].values())[1:]
  except :
    print("generating")
    result = spoty(track_name,tag,url)


      # Update the existing dictionary with new data
    new_data = {
        url: {
            "soundcloud_link": result[0],
            "spotify_name": result[1],
            "spotify_url": result[2],
            "competitor_track": result[3],
            "competitor": result[4],
            "comp_url": result[5],
        }
    }
    loaded_data.update(new_data)

  return result


def spoty(track_name,tag,url):
    track_name = remove_bracket_content(track_name)
    results = search_spotify_albums(track_name, client_ids, client_secrets)
    if results["tracks"]["total"] > 0:
        track = results["tracks"]["items"][0]
        spot_name = track["name"]
        spot_url = track["href"]
        spot_url = "https://open.spotify.com/track/" + spot_url.split("/")[-1]

    else:
        spot_name = None
        spot_url = None

        # Example: Search for a track and retrieve its information
    track_name = track_name + f" {tag}"
    results = search_spotify_albums(track_name, client_ids, client_secrets)

    if results["tracks"]["total"] > 0:
        track = results["tracks"]["items"][0]
        comp_name = track["name"]
        comp_artist = track["artists"][0]["name"]
        comp_url = track["href"]
        comp_url = "https://open.spotify.com/track/" + comp_url.split("/")[-1]

    else:
        comp_name = None
        comp_url = None
        comp_artist = None


    return [url,spot_name, spot_url, comp_name, comp_artist, comp_url]




def extract_dictionary_from_html(url):
    try:
        soup = create_soup_from_html(url)
        script_tags = soup.find_all("script")
    except:
        try:
            soup = create_soup_from_html(url)
            script_tags = soup.find_all("script")
        except:
            pass

    for script in script_tags:
        if "__sc_hydration" in str(script):
            data_start = str(script).find("[{")
            data_end = str(script).rfind("}]") + 2
            json_data = str(script)[data_start:data_end]
            data_dict = json.loads(json_data)
            return data_dict

def remove_bracket_content(input_string):
    pattern = r"\([^()]*\)"
    return re.sub(pattern, "", input_string)

