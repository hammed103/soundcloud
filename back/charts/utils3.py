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
    "19f14f0876b9481284eb571cd293f62f",
    "789485697b90489f9a6825544fa5fda5",
    "54246611cfd4443fa5aee8dc9bf6f750",
    "2a3d2700ca0b432eb31035189502a54b",
    "8c47da1ab9fd407880923d77390571e4",
    "e7811ed904434f8a85295e7f33e7eced",
    "6e45323f50bb4ab99de699d13770801c",
    "2c98e1d916ad4833b9ada7863b0a22fb",
    "25abaa3f24e2456ca085254feea646b3",
    "50ee1d5e3a0e4cf4baa40cd9c287629d",
    "a9ecebb55f0c48388ca5d1a98e7164e8",
    "32d7c2dcba13414bbae9953aa80ec0db",
    "bd8fbf3344e04d8bbba162d2009cc8ad",
    "f201fae4c33f44059296972700d2570f",
    "400ed1c70ace4f1b91b4501a04107d19",
    "3ae73d0e0d0c4d0fa72905478a3fbb65",
    "54e4e63a02884f0b8ae3499437e5035a",
    "e88001ff755d418daa3a6b0be9b5f10a",
    "356b3baf2a264058a66948b66f641a4c",
    "fe7d463857cc4448b47b91db89d944d0",
    "da8d6c2a1f0e416e8e8dc5ecad006272",
    "d19671d4b00b404d9c61bb770f4e2c05",
    "cabcaeba05fa40d7a1d582310c809ec8",
    "a56850ca13c34e9b84ce524d48d23345",
    "8906d085637b4a79a3a74fbd2822809d",
    "cd44afaf9d4a491e89128c831e9e75d2",
    "beff3627c4aa48388b60f685385c8d3d",
    "656e6b548d0b4afebfa7e431fe8ca402",
    "36b8fd757bcb4395ab11fd4c8e542875",
    "4f56b40d54fd4022bc49b3e13da8e7d5",
    "d80d4d7c091646e58c8fbd68104dfbdc",
    "06a37fa6a47e492b889fef58a213a7de",
    "152f12572dc84cb38e3728343a10bd38",
    "7a48ef97d45d492daaf29fecbf731e5a",
    "c1754b38145d46a89a44d0c62d41214b",
    "174aaba9f3c14c0da0dd2b95bbbb2c2f",
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
    "2ce7211877264a4b8f9b17056c31de30",
    "aff8593042e9411eb27f77a276fcc643",
    "e4d931fe4c8d48dabeba8aee8d1f2c21",
    "279db43fc0444f5b9803d82f8a697829",
    "5fc1930151c74bf585f57ee439feec2c",
    "b8038c07fe024faeb53bebe7c59a3805",
    "5ee72b7713c74bc09de5facb344ef996",
    "0025b5644ff647b581c658831f5160de",
    "e5fc858aa00e481084fe1670e4ba9fd2",
    "3ced030cb1584c15a6d4a7c0a31975ac",
    "e33e7c5dfe654de3a2cb24f4c2cb5acc",
    "f66b47037f844ce69def55eb262108d8",
    "4d70422d688d4f41a66baf786f68acb8",
    "9dbd5ed4a52242c29543367c620a189a",
    "37443193df204aab8cc2ef6d6ae16995",
    "a88ece523f69485d9712b08ac44abfc5",
    "0e98b65864354ae8b8ed7d246d4b26af",
    "770bb549d7824f16938231fa21eb5c93",
    "ca0d813f7d214764992d6a260137dcb2",
    "48b7ac2198364a38ab9bfc4e824a70fb",
    "f19605e708ec42939da1ae87c9f80d74",
    "a4210ae69c4242d690acc8bbbe56fd0a",
    "71d93c5f0796468186e729d976ca8e8c",
    "97a9936ef65b4abcb7b825a1123ce2ff",
    "babf2579894f4993a806d5b749aec583",
    "5b854f267dff42619246cd7891f1f0ca",
    "e5881637633743fea497ff0e1aee84cd",
    "cf45e4019f5341d598a3cdd05f7cddea",
    "e5c6b30a4d294504872de3f02e321617",
    "ddfe7bac79704403b96ca5fc85acb5ee",
    "62cdebb65fbd45a48d390b83c913aa1e",
    "1a30bad5969a47d893a72f6cc8d61605",
    "c3b4c73959a04469a19449ac2236a450",
    "ce114a1ae82c45ddaf1aa98d1c9d42f6",
    "2b33680560874b9596eef04739d58028",
    "a393141befe64c4aab8d92e86841571a",
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


def search_spotify_albums(query, client_ids, client_secrets, max_attempts=30):
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


def book(track_name, tag, url, uri):
    global loaded_data
    try:
        result = list(loaded_data[url].values())
        if len(result) != 7:
            print("incept")
            sdf
    except:
        try:
            print("generating")
            result = spoty(track_name, tag, url, uri)
            if len(result) != 7:
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
                    "uri": uri,
                }
            }
            print(new_data)
            loaded_data.update(new_data)

            print(len(loaded_data))
        except:

            print("Need to rerun")
            result = ["", "", "", "", "", "", ""]

    return result[1:-1]


def spoty(track_name, tag, url, uri):
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

    return [url, spot_name, spot_url, comp_name, comp_artist, comp_url, uri]


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


import re


def remove_brackets(s):
    # Remove content inside and including round brackets ()
    s = re.sub(r"\(.*?\)", "", s)

    # Remove content inside and including square brackets []
    s = re.sub(r"\[.*?\]", "", s)

    return s.strip()


def search_spotify_albums_country(
    query, cd, client_ids, client_secrets, max_attempts=30
):
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
            "market": cd,
            "limit": "50",
        }
        max_retries = 5
        retry_delay = 2  # delay in seconds
        response = None

        for i in range(max_retries):
            try:
                response = requests.get(
                    "https://api.spotify.com/v1/search", params=params, headers=headers
                )

                break
            except:
                if i < max_retries - 1:  # Don't sleep after the last retry
                    sleep(retry_delay)

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


def convert_ms_to_mm_ss(duration_ms):
    # Convert total milliseconds to total seconds
    total_seconds = duration_ms // 1000

    # Calculate minutes and seconds
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # Format and return as mm:ss
    return f"{minutes:02}:{seconds:02}"


# Example usage
duration_ms = 185000
formatted_time = convert_ms_to_mm_ss(duration_ms)
print(formatted_time)  # Expected output: 3:05


output_pairs = [
    ("STAY - STUTTER", "stay stutter"),
    ("STAY - STUTTER SPED UP", "stay stutter"),
    ("STAY - STUTTER SPED UP", "stay stutter sped up"),
    ("STAY - STUTTER SLOWED + REVERB", "stay stutter"),
    ("STAY - STUTTER SLOWED + REVERB", "stay stutter slowed + reverb"),
    ("SOME SAY - STUTTER", "some say stutter"),
    ("SOME SAY - STUTTER SPED UP", "some say stutter"),
    ("SOME SAY - STUTTER SPED UP", "some say stutter sped up"),
    ("SOME SAY - STUTTER SLOWED + REVERB", "some say stutter"),
    ("SOME SAY - STUTTER SLOWED + REVERB", "some say stutter slowed + reverb"),
    ("I LOVE YOU - STUTTER", "i love you stutter"),
    ("I LOVE YOU - STUTTER SPED UP", "i love you stutter"),
    ("I LOVE YOU - STUTTER SPED UP", "i love you stutter sped up"),
    ("I LOVE YOU - STUTTER SLOWED + REVERB", "i love you stutter"),
    ("I LOVE YOU - STUTTER SLOWED + REVERB", "i love you stutter slowed + reverb"),
    ("FORMULA - STUTTER", "formula stutter"),
    ("FORMULA - STUTTER SPED UP", "formula stutter"),
    ("FORMULA - STUTTER SPED UP", "formula stutter sped up"),
    ("FORMULA - STUTTER SLOWED + REVERB", "formula stutter"),
    ("FORMULA - STUTTER SLOWED + REVERB", "formula stutter slowed + reverb"),
    ("YOU'RE SOMEBODY ELSE - STUTTER", "you're somebody else stutter"),
    ("YOU'RE SOMEBODY ELSE - STUTTER SPED UP", "you're somebody else stutter"),
    ("YOU'RE SOMEBODY ELSE - STUTTER SPED UP", "you're somebody else stutter sped up"),
    ("YOU'RE SOMEBODY ELSE - STUTTER SLOWED + REVERB", "you're somebody else stutter"),
    (
        "YOU'RE SOMEBODY ELSE - STUTTER SLOWED + REVERB",
        "you're somebody else stutter slowed + reverb",
    ),
    ("WE FOUND LOVE - STUTTER", "we found love stutter"),
    ("WE FOUND LOVE - STUTTER SPED UP", "we found love stutter"),
    ("WE FOUND LOVE - STUTTER SPED UP", "we found love stutter sped up"),
    ("WE FOUND LOVE - STUTTER SLOWED + REVERB", "we found love stutter"),
    (
        "WE FOUND LOVE - STUTTER SLOWED + REVERB",
        "we found love stutter slowed + reverb",
    ),
    ("THINKING ABOUT YOU - STUTTER", "thinking about you stutter"),
    ("THINKING ABOUT YOU - STUTTER SPED UP", "thinking about you stutter"),
    ("THINKING ABOUT YOU - STUTTER SPED UP", "thinking about you stutter sped up"),
    ("THINKING ABOUT YOU - STUTTER SLOWED + REVERB", "thinking about you stutter"),
    (
        "THINKING ABOUT YOU - STUTTER SLOWED + REVERB",
        "thinking about you stutter slowed + reverb",
    ),
    ("SET FIRE TO THE RAIN - STUTTER", "set fire to the rain stutter"),
    ("SET FIRE TO THE RAIN - STUTTER SPED UP", "set fire to the rain stutter"),
    ("SET FIRE TO THE RAIN - STUTTER SPED UP", "set fire to the rain stutter sped up"),
    ("SET FIRE TO THE RAIN - STUTTER SLOWED + REVERB", "set fire to the rain stutter"),
    (
        "SET FIRE TO THE RAIN - STUTTER SLOWED + REVERB",
        "set fire to the rain stutter slowed + reverb",
    ),
    ("SAY IT RIGHT - STUTTER", "say it right stutter"),
    ("SAY IT RIGHT - STUTTER SPED UP", "say it right stutter"),
    ("SAY IT RIGHT - STUTTER SPED UP", "say it right stutter sped up"),
    ("SAY IT RIGHT - STUTTER SLOWED + REVERB", "say it right stutter"),
    ("SAY IT RIGHT - STUTTER SLOWED + REVERB", "say it right stutter slowed + reverb"),
    ("NUMB - STUTTER", "numb stutter"),
    ("NUMB - STUTTER SPED UP", "numb stutter"),
    ("NUMB - STUTTER SPED UP", "numb stutter sped up"),
    ("NUMB - STUTTER SLOWED + REVERB", "numb stutter"),
    ("NUMB - STUTTER SLOWED + REVERB", "numb stutter slowed + reverb"),
    ("NEVER LET ME DOWN - STUTTER", "never let me down stutter"),
    ("NEVER LET ME DOWN - STUTTER SPED UP", "never let me down stutter"),
    ("NEVER LET ME DOWN - STUTTER SPED UP", "never let me down stutter sped up"),
    ("NEVER LET ME DOWN - STUTTER SLOWED + REVERB", "never let me down stutter"),
    (
        "NEVER LET ME DOWN - STUTTER SLOWED + REVERB",
        "never let me down stutter slowed + reverb",
    ),
    ("MANEATER - STUTTER", "maneater stutter"),
    ("MANEATER - STUTTER SPED UP", "maneater stutter"),
    ("MANEATER - STUTTER SPED UP", "maneater stutter sped up"),
    ("MANEATER - STUTTER SLOWED + REVERB", "maneater stutter"),
    ("MANEATER - STUTTER SLOWED + REVERB", "maneater stutter slowed + reverb"),
    ("LOVE TONIGHT - STUTTER", "love tonight stutter"),
    ("LOVE TONIGHT - STUTTER SPED UP", "love tonight stutter"),
    ("LOVE TONIGHT - STUTTER SPED UP", "love tonight stutter sped up"),
    ("LOVE TONIGHT - STUTTER SLOWED + REVERB", "love tonight stutter"),
    ("LOVE TONIGHT - STUTTER SLOWED + REVERB", "love tonight stutter slowed + reverb"),
    ("LET YOU GO - STUTTER", "let you go stutter"),
    ("LET YOU GO - STUTTER SPED UP", "let you go stutter"),
    ("LET YOU GO - STUTTER SPED UP", "let you go stutter sped up"),
    ("LET YOU GO - STUTTER SLOWED + REVERB", "let you go stutter"),
    ("LET YOU GO - STUTTER SLOWED + REVERB", "let you go stutter slowed + reverb"),
    ("LEFT OUTSIDE ALONE - STUTTER", "left outside alone stutter"),
    ("LEFT OUTSIDE ALONE - STUTTER SPED UP", "left outside alone stutter"),
    ("LEFT OUTSIDE ALONE - STUTTER SPED UP", "left outside alone stutter sped up"),
    ("LEFT OUTSIDE ALONE - STUTTER SLOWED + REVERB", "left outside alone stutter"),
    (
        "LEFT OUTSIDE ALONE - STUTTER SLOWED + REVERB",
        "left outside alone stutter slowed + reverb",
    ),
    ("JUST DANCE - STUTTER", "just dance stutter"),
    ("JUST DANCE - STUTTER SPED UP", "just dance stutter"),
    ("JUST DANCE - STUTTER SPED UP", "just dance stutter sped up"),
    ("JUST DANCE - STUTTER SLOWED + REVERB", "just dance stutter"),
    ("JUST DANCE - STUTTER SLOWED + REVERB", "just dance stutter slowed + reverb"),
    ("JUDAS - STUTTER", "judas stutter"),
    ("JUDAS - STUTTER SPED UP", "judas stutter"),
    ("JUDAS - STUTTER SPED UP", "judas stutter sped up"),
    ("JUDAS - STUTTER SLOWED + REVERB", "judas stutter"),
    ("JUDAS - STUTTER SLOWED + REVERB", "judas stutter slowed + reverb"),
    ("JERICHO - STUTTER", "jericho stutter"),
    ("JERICHO - STUTTER SPED UP", "jericho stutter"),
    ("JERICHO - STUTTER SPED UP", "jericho stutter sped up"),
    ("JERICHO - STUTTER SLOWED + REVERB", "jericho stutter"),
    ("JERICHO - STUTTER SLOWED + REVERB", "jericho stutter slowed + reverb"),
    ("I'M AN ALBATRAOZ - STUTTER", "i'm an albatraoz stutter"),
    ("FLOWERS - STUTTER", "flowers stutter"),
    ("FLOWERS - STUTTER SPED UP", "flowers stutter"),
    ("FLOWERS - STUTTER SPED UP", "flowers stutter sped up"),
    ("FLOWERS - STUTTER SLOWED + REVERB", "flowers stutter"),
    ("FLOWERS - STUTTER SLOWED + REVERB", "flowers stutter slowed + reverb"),
    ("DO YOU MISS ME? - STUTTER", "do you miss me? stutter"),
    ("DO YOU MISS ME? - STUTTER SPED UP", "do you miss me? stutter"),
    ("DO YOU MISS ME? - STUTTER SPED UP", "do you miss me? stutter sped up"),
    ("DO YOU MISS ME? - STUTTER SLOWED + REVERB", "do you miss me? stutter"),
    (
        "DO YOU MISS ME? - STUTTER SLOWED + REVERB",
        "do you miss me? stutter slowed + reverb",
    ),
    ("DISTURBIA - STUTTER", "disturbia stutter"),
    ("DISTURBIA - STUTTER SPED UP", "disturbia stutter"),
    ("DISTURBIA - STUTTER SPED UP", "disturbia stutter sped up"),
    ("DISTURBIA - STUTTER SLOWED + REVERB", "disturbia stutter"),
    ("DISTURBIA - STUTTER SLOWED + REVERB", "disturbia stutter slowed + reverb"),
    ("CAN'T GET YOU OUT OF MY HEAD - STUTTER", "can't get you out of my head stutter"),
    (
        "CAN'T GET YOU OUT OF MY HEAD - STUTTER SPED UP",
        "can't get you out of my head stutter",
    ),
    (
        "CAN'T GET YOU OUT OF MY HEAD - STUTTER SPED UP",
        "can't get you out of my head stutter sped up",
    ),
    (
        "CAN'T GET YOU OUT OF MY HEAD - STUTTER SLOWED + REVERB",
        "can't get you out of my head stutter",
    ),
    (
        "CAN'T GET YOU OUT OF MY HEAD - STUTTER SLOWED + REVERB",
        "can't get you out of my head stutter slowed + reverb",
    ),
    ("BELLY DANCER - STUTTER", "belly dancer stutter"),
    ("BELLY DANCER - STUTTER SPED UP", "belly dancer stutter"),
    ("BELLY DANCER - STUTTER SPED UP", "belly dancer stutter sped up"),
    ("BELLY DANCER - STUTTER SLOWED + REVERB", "belly dancer stutter"),
    ("BELLY DANCER - STUTTER SLOWED + REVERB", "belly dancer stutter slowed + reverb"),
    ("BARBIE GIRL - STUTTER", "barbie girl stutter"),
    ("BARBIE GIRL - STUTTER SPED UP", "barbie girl stutter"),
    ("BARBIE GIRL - STUTTER SPED UP", "barbie girl stutter sped up"),
    ("BARBIE GIRL - STUTTER SLOWED + REVERB", "barbie girl stutter"),
    ("BARBIE GIRL - STUTTER SLOWED + REVERB", "barbie girl stutter slowed + reverb"),
    ("ANOTHER LOVE - STUTTER", "another love stutter"),
    ("ANOTHER LOVE - STUTTER SPED UP", "another love stutter"),
    ("ANOTHER LOVE - STUTTER SPED UP", "another love stutter sped up"),
    ("ANOTHER LOVE - STUTTER SLOWED + REVERB", "another love stutter"),
    ("ANOTHER LOVE - STUTTER SLOWED + REVERB", "another love stutter slowed + reverb"),
    ("ALL AROUND THE WORLD  - STUTTER", "all around the world  stutter"),
    ("ALL AROUND THE WORLD  - STUTTER SPED UP", "all around the world  stutter"),
    (
        "ALL AROUND THE WORLD  - STUTTER SPED UP",
        "all around the world  stutter sped up",
    ),
    (
        "ALL AROUND THE WORLD  - STUTTER SLOWED + REVERB",
        "all around the world  stutter",
    ),
    (
        "ALL AROUND THE WORLD  - STUTTER SLOWED + REVERB",
        "all around the world  stutter slowed + reverb",
    ),
    ("STRANGERS - STUTTER", "strangers stutter"),
    ("STRANGERS - STUTTER SPED UP", "strangers stutter"),
    ("STRANGERS - STUTTER SPED UP", "strangers stutter sped up"),
    ("STRANGERS - STUTTER SLOWED + REVERB", "strangers stutter"),
    ("STRANGERS - STUTTER SLOWED + REVERB", "strangers stutter slowed + reverb"),
    ("toca toca - sped up", "toca toca "),
    ("toca toca - sped up", "toca toca sped up"),
]
