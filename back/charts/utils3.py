import pandas as pd
import requests
from datetime import datetime
import base64
from bs4 import BeautifulSoup

# List of client IDs and client secrets
client_ids = [
    "53fb1dbe5f42480ba654fcc3c7e168d6",
    "cb7eb4ee66a543dab0c56e3e8db63475",
    "20f25a5cbcb84d998d91ec0e29529b0e",
    "ab3f711fb94e43c29f107504e2bc6c2e",
    "39381b8f10524649a65923eb264f55c1",
    "f7c3b2637f704afeb838c3a9ebbfa03e",
    "54dedd34f984442c947908eab4cba6b0",
    "986c04f81f4141f1913ffd08efaaa2ef",
]
client_secrets = [
    "5c1da4cce90f410e88966cdfc0785e3a",
    "2d5ea5e9d05945ec92bcf0bbe837c573",
    "f773eee78b76468098da352c669228d8",
    "3ac0d4cc5622440ca60a1dee3c0c1e9f",
    "56f690af59db4b53a6fa3ebb0b5398fa",
    "f7c3b2637f704afeb838c3a9ebbfa03e",
    "4b757ab77672427198059aac1344951b",
    "45179b3aef4949c38f37c50a0a8d803c",
]

import json
import os
from django.conf import settings

# Set your client key and secret

# json_file_path =  r"C:\Users\SteelSeries\Desktop\Upwork\Alex M\cloud\top50chart\back\charts\statiic\grouped_data.json"
static_folder = settings.STATIC_ROOT
json_file_path = os.path.join(static_folder, "grouped_data.json")

# Read the JSON file and convert it into a dictionary
with open(json_file_path, "r") as json_file:
    loaded_data = json.load(json_file)


def create_soup_from_html(url):
    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 Edg/115.0.1901.203",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None


def get_access_token(client_id, client_secret):
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


def search_spotify_albums(query, client_ids, client_secrets, max_attempts=8):
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
            print(
                f"Attempt {attempt + 1}: Request failed with status code {response.status_code}"
            )

            if attempt < max_attempts - 1:
                print("Retrying...")
            else:
                print("Max attempts reached. Giving up.")
                return None


import re


def book(track_name, tag, url,uri):
    global loaded_data
    try:
        result = list(loaded_data[url].values())
        if len(result) != 7 :
            print("incept")
            sdf
    except:
        try:
            print("generating")
            result = spoty(track_name, tag, url,uri)
            if len(result) != 7 :
                print("decept")
                sdf

            # Update the existing dictionary with new data
            new_data = {
                url: {
                    "soundcloud_link": result[0],
                    "spotify_name": result[1],
                    "spotify_url": result[2],
                    "competitor_track": result[3],
                    "competitor": result[4],
                    "comp_url": result[5],
                     "uri":uri,
                }
            }
            print(new_data)
            loaded_data.update(new_data)

            print(len(loaded_data))
        except:

            print("Need to rerun")
            result = ["", "", "", "", "", "",""]
           
            

    return result[1:-1]


def spoty(track_name, tag, url,uri):
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

    return [url, spot_name, spot_url, comp_name, comp_artist, comp_url,uri]


import json


from time import sleep


def extract_dictionary_from_html(url):
    print(url)
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
        # print(script)
        # print("viavle")
        if "__sc_hydration" in str(script):
            # print(str(script))
            data_start = str(script).find("[{")
            data_end = str(script).rfind("}]") + 2
            json_data = str(script)[data_start:data_end]

            data_dict = json.loads(json_data)
            dummy = [str(i["id"]) for i in data[6]["data"]["tracks"]]

            return dummy

        if "NEXT" in str(script):
            # print("found")
            data = str(script)
            # Use regular expression to find all track IDs
            track_ids = re.findall(r'"soundcloud:tracks:(\d+)"', data)
            track_ids = [x for i, x in enumerate(track_ids) if x not in track_ids[:i]]
            print(len(track_ids))

            return track_ids


def remove_bracket_content(input_string):
    pattern = r"\([^()]*\)"
    return re.sub(pattern, "", input_string)



def split_dict_equally(data, parts=3):
    """Split a dictionary into n parts."""
    new_data = [{} for _ in range(parts)]
    items = list(data.items())
    
    for i, item in enumerate(items):
        new_data[i % parts][item[0]] = item[1]

    return new_data




def save_data():
    print(len(loaded_data))
    with open(json_file_path, "w") as json_file:
        json.dump(loaded_data, json_file, indent=4)