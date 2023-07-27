from .models import Chart, Chart_disc
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re


def remove_bracket_content(input_string):
    pattern = r"\([^()]*\)"
    return re.sub(pattern, "", input_string)


# Set your client key and secret
client_id = "53fb1dbe5f42480ba654fcc3c7e168d6"
client_secret = "5c1da4cce90f410e88966cdfc0785e3a"


import requests
import base64



def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    
    # Encode the client_id and client_secret using base64
    credentials = f"{client_id}:{client_secret}"
    credentials_bytes = credentials.encode('ascii')
    credentials_base64 = base64.b64encode(credentials_bytes).decode('ascii')
    
    headers = {'Authorization': 'Basic ' + credentials_base64}
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        # Use the access_token for your API requests
        print(f'Access Token: {access_token}')
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return access_token
# Initialize the Spotify client

def search_spotify_albums(query, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    url = f'https://api.spotify.com/v1/search'
    params = {
        'q': query,
        'type': 'track',
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
access_token = get_access_token()
# views.py
from django.shortcuts import HttpResponse
from datetime import timedelta
from time import sleep
import requests

headers = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
}

from bs4 import BeautifulSoup


def get_country_code(country_name):
    return next(
        (
            code
            for country, code in countries_tuple
            if country.lower() == country_name.lower()
        ),
        None,
    )


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


import json

countries_tuple = [
    ("Germany", "DE"),
    ("United Kingdom", "GB"),
    ("United States", "US"),
    ("Netherlands", "NL"),
    ("France", "FR"),
    ("Australia", "AU"),
    ("Brazil", "BR"),
    ("Poland", "PL"),
    ("Sweden", "SE"),
    ("Austria", "AT"),
    ("India", "IN"),
    ("Canada", "CA"),
    ("Turkey", "TR"),
    ("Switzerland", "CH"),
    ("Norway", "NO"),
    ("Indonesia", "ID"),
    ("Mexico", "MX"),
    ("New Zealand", "NZ"),
    ("Belgium", "BE"),
    ("Ireland", "IE"),
    ("Italy", "IT"),
    ("Portugal", "PT"),
    ("Spain", "ES"),
    ("Denmark", "DK"),
    ("Finland", "FI"),
]


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


def spoty(current_chart):
    print("a")
    track_name = current_chart["title"]
    tag = current_chart["tags"]
    track_name = remove_bracket_content(track_name)
    results =  search_spotify_albums(track_name, access_token)
    print("b")
    if results["tracks"]["total"] > 0:
        track = results["tracks"]["items"][0]
        spot_name = track["name"]
        spot_url = track["href"]
        spot_url = "https://open.spotify.com/track/" + spot_url.split("/")[-1]

    else:
        spot_name = None
        spot_url = None

        # Example: Search for a track and retrieve its information
    track_name = current_chart["title"] + f" {tag}"
    results = sp.search(q=track_name, type="track", limit=1)

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

    return spot_name, spot_url, comp_name, comp_artist, comp_url


def generate_discover(current_charts):
    for current_chart in current_charts:
        sleep(1)
        try:
            # Try to get the existing entry for the song based on unique fields
            song = Chart_disc.objects.get(
                title=current_chart["title"],
                tags=current_chart["tags"],
                country=current_chart["country"],
                today=current_chart["date"],
            )

            # Update the existing entry with new data
            song.current_position = current_chart["current_position"]
            song.link = current_chart["link"]
            song.sound_likes = current_chart["sound_likes"]
            song.sound_play = current_chart["sound_play"]
            song.sound_repost = current_chart["sound_repost"]
            song.sound_release = current_chart["sound_release"]

            # Calculate previous_position and position_7_days_ago
            yesterday = current_chart["date"] - timedelta(days=1)
            last_week = current_chart["date"] - timedelta(weeks=1)

            try:
                previous_entry = Chart_disc.objects.get(
                    title=current_chart["title"],
                    tags=current_chart["tags"],
                    country=current_chart["country"],
                    today=yesterday,
                )
                song.previous_position = previous_entry.current_position
            except Chart_disc.DoesNotExist:
                # If there's no entry for yesterday, set previous_position to None
                song.previous_position = None

            try:
                last_week_entry = Chart_disc.objects.get(
                    title=current_chart["title"],
                    tags=current_chart["tags"],
                    country=current_chart["country"],
                    today=last_week,
                )
                song.position_7_days_ago = last_week_entry.current_position
            except Chart_disc.DoesNotExist:
                # If there's no entry for last week, set position_7_days_ago to None
                song.position_7_days_ago = None

            song.save()

        except Chart_disc.DoesNotExist:

            try:
                song = Chart.objects.filter(
                    title=current_chart["title"],
                ).first()
                comp_artist = song.comp_artist
                comp_name = song.comp_name
                comp_url = song.comp_url
                spot_url = song.spot_url
                spot_name = song.spot_name

            except:
                print("new xxxx")
                spot_name, spot_url, comp_name, comp_artist, comp_url = spoty(
                    current_chart=current_chart
                )
                print("out")

            # Example: Search for a track and retrieve its information

            # Create a new entry if it doesn't exist
            Chart_disc.objects.create(
                tags=current_chart["tags"],
                country=current_chart["country"],
                current_position=current_chart["current_position"],
                title=current_chart["title"],
                link=current_chart["link"],
                sound_likes=current_chart["sound_likes"],
                sound_play=current_chart["sound_play"],
                sound_repost=current_chart["sound_repost"],
                sound_release=current_chart["sound_release"],
                today=current_chart["date"],
                comp_artist=comp_artist,
                comp_name=comp_name,
                comp_url=comp_url,
                spot_name=spot_name,
                spot_url=spot_url,
            )


def generate(current_charts):
    for current_chart in current_charts[:]:
        print(current_chart)
        sleep(1)
        try:
            # Try to get the existing entry for the song based on unique fields
            song = Chart.objects.get(
                title=current_chart["title"],
                tags=current_chart["tags"],
                today=current_chart["date"],
            )

            # Update the existing entry with new data
            song.current_position = current_chart["current_position"]
            song.link = current_chart["link"]
            song.sound_likes = current_chart["sound_likes"]
            song.sound_play = current_chart["sound_play"]
            song.sound_repost = current_chart["sound_repost"]
            song.sound_release = current_chart["sound_release"]

            # Calculate previous_position and position_7_days_ago
            yesterday = current_chart["date"] - timedelta(days=1)
            last_week = current_chart["date"] - timedelta(weeks=1)
            print(yesterday)
            

            try:
                previous_entry = Chart.objects.get(
                    title=current_chart["title"],
                    tags=current_chart["tags"],
                    today=yesterday,
                )
                song.previous_position = previous_entry.current_position
                
            except Chart.DoesNotExist:
                # If there's no entry for yesterday, set previous_position to None
                song.previous_position = None
            print(song.previous_position)
            print(song.current_position)
            try:
                last_week_entry = Chart.objects.get(
                    title=current_chart["title"],
                    tags=current_chart["tags"],
                    today=last_week,
                )
                song.position_7_days_ago = last_week_entry.current_position
            except Chart.DoesNotExist:
                # If there's no entry for last week, set position_7_days_ago to None
                song.position_7_days_ago = None

            song.save()

        except Chart.DoesNotExist:
            try:
                song = Chart.objects.filter(
                    title=current_chart["title"],
                    tags=current_chart["tags"],
                ).first()
                comp_artist = song.comp_artist
                comp_name = song.comp_name
                comp_url = song.comp_url
                spot_url = song.spot_url
                spot_name = song.spot_name

            except:
                print("new xxxx")
                spot_name, spot_url, comp_name, comp_artist, comp_url = spoty(
                    current_chart=current_chart
                )

            # Example: Search for a track and retrieve its information

            # Create a new entry if it doesn't exist
            Chart.objects.create(
                tags=current_chart["tags"],
                current_position=current_chart["current_position"],
                title=current_chart["title"],
                link=current_chart["link"],
                sound_likes=current_chart["sound_likes"],
                sound_play=current_chart["sound_play"],
                sound_repost=current_chart["sound_repost"],
                sound_release=current_chart["sound_release"],
                today=current_chart["date"],
                comp_artist=comp_artist,
                comp_name=comp_name,
                comp_url=comp_url,
                spot_name=spot_name,
                spot_url=spot_url,
            )
