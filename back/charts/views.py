from django.shortcuts import render
from .models import Chart
import requests
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework.views import APIView
from bs4 import BeautifulSoup
import re




def extract_tiktok_username(url):
    # Split the URL using the '/' character
    parts = url.split('/')

    # Find the part of the URL containing '@' followed by the username
    for part in parts:
        if part.startswith('@'):
            return part

    # If no '@' symbol followed by username is found, return None
    return None

def loader(url) :

  url = f"{url}"

  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

  response = requests.get(url, headers=headers)

  tiktok_username = extract_tiktok_username(response.url)
  url = f"https://www.tiktok.com/{tiktok_username}"
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      # Extracting the profile/bio information from the HTML
      user_info = {}
      user_info['username'] = tiktok_username
      nm = soup.find('div', class_=re.compile(r'DivShareTitleContainer'))
      user_info['title']   = nm.find("h1").text
      user_info['subtitle']   = nm.find("h2").text
      inf = soup.find('div', class_=re.compile(r'DivShareLayoutHeader'))
      user_info['followers'] = inf.find_all("strong")[1].text
      user_info['following'] = inf.find_all("strong")[0].text
      user_info["likes"] = inf.find_all("strong")[2].text
      user_info["image"] = inf.find("img")["src"]
      user_info["bio"] = soup.find('h2', class_=re.compile(r'H2ShareDesc')).text
      user_info["external_link"] = soup.find('div', class_=re.compile(r'DivShareLinks')).text

  return user_info

def generate_top_50(current_chart):
    # Get the previous top 50 chart
    previous_chart = Chart.objects.order_by("current_position")
    # Write to .json file
    # Create a dictionary to store the song positions
    song_positions = {}

    # Populate the song_positions dictionary with previous positions
    for i, song in enumerate(previous_chart, start=1):
        song_positions[(song.title, song.tags)] = (song.current_position, None)

    # Update the song_positions dictionary with current positions and update database
    for i, song in enumerate(current_chart, start=1):
        song_tags = song["tags"]
        song_title = song["title"]
        curr_pos = song["current_position"]
        sound_play = song["sound_play"]
        sound_likes = song["sound_likes"]
        sound_repost = song["sound_repost"]
        sound_release = song["sound_release"]
        lastweek = song["lastweek"]
        link = song["link"]
        if (song_title, song_tags) in song_positions:
            prev_pos, _ = song_positions[(song_title, song_tags)]
            print((song_title, song_tags))
            chart_obj = Chart.objects.get(title=song_title, tags=song_tags)
            chart_obj.previous_position = prev_pos
            chart_obj.current_position = curr_pos
            chart_obj.indicator = prev_pos - curr_pos
            chart_obj.sound_play = sound_play
            chart_obj.sound_likes = sound_likes
            chart_obj.sound_repost = sound_repost
            chart_obj.sound_release = sound_release
            chart_obj.lastweek = lastweek
            print(prev_pos - curr_pos)
            chart_obj.link = link
            chart_obj.save()
        else:
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials

            import re

            def remove_bracket_content(input_string):
                pattern = r"\([^()]*\)"
                return re.sub(pattern, "", input_string)

            # Set your client key and secret
            client_id = "53fb1dbe5f42480ba654fcc3c7e168d6"
            client_secret = "5c1da4cce90f410e88966cdfc0785e3a"

            # Initialize the Spotify client
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            # Example: Search for a track and retrieve its information
            track_name = song_title
            track_name = remove_bracket_content(track_name)
            results = sp.search(q=track_name, type="track", limit=1)

            if results["tracks"]["total"] > 0:
                track = results["tracks"]["items"][0]
                spot_name = track["name"]
                spot_url = track["href"]
                spot_url = "https://open.spotify.com/track/" + spot_url.split("/")[-1]

            else:
                spot_name = None
                spot_url = None

                # Example: Search for a track and retrieve its information
            track_name = song_title + " hardstyle"
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

            # Add the new song to the database
            chart_obj = Chart(
                title=song_title,
                previous_position=None,
                current_position=curr_pos,
                indicator=None,
                lastweek=lastweek,
                link=link,
                spot_name=spot_name,
                spot_url=spot_url,
                comp_name=comp_name,
                comp_url=comp_url,
                comp_artist=comp_artist,
                sound_likes=sound_likes,
                sound_play=sound_play,
                sound_repost=sound_repost,
                sound_release=sound_release,
                tags=song_tags,
            )
            chart_obj.save()


class Render(APIView):
    @staticmethod
    def get(request):

        # tags = request.data["tags"]
        previous_chart = Chart.objects.order_by("current_position")

        # Convert QuerySet to list of dictionaries
        previous_chart_list = [model_to_dict(instance) for instance in previous_chart]

        return Response(
            {
                "status": "success",
                "data": previous_chart_list,
            },
            status=201,
        )
    

class tik(APIView):
    @staticmethod
    def post(request):

        result = loader(request.url)
        return Response(
            {
                "status": "success",
                "data": result,
            },
            status=201,


class Update(APIView):
    @staticmethod
    def get(req):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Origin": "https://soundcloud.com",
            "Referer": "https://soundcloud.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/114.0.0.0",
        }
        current_charts = []

        for tag in [
            "hardstyle",
            "tekkno",
            "hardtekk",
            "tekk",
            "drill",
            "phonk",
            "lofi",
            "lo-fi",
            "tiktok",
            "sped-up",
            "spedup",
            "slowed",
            "remix",
            "viral",
            "hardtechno",
        ]:
            response = requests.get(
                f"https://api-v2.soundcloud.com/search/tracks?q=*&filter.genre_or_tag={tag}&sort=popular&client_id=w2Cs8NzMrJqhjiCIinZ1xxNBqPNgTVIe&limit=50&offset=0&linked_partitioning=1&app_version=1689322736&app_locale=en",
                headers=headers,
            )
            dt = response.json()
            current_chart = [
                {
                    "tags": tag,
                    "lastweek": None,
                    "current_position": index + 1,
                    "title": i["title"],
                    "link": i["permalink_url"],
                    "sound_likes": i["likes_count"],
                    "sound_play": i["playback_count"],
                    "sound_repost": i["reposts_count"],
                    "sound_release": i["display_date"],
                }
                for index, i in enumerate(dt["collection"])
            ][:51]

            current_charts += current_chart

        generate_top_50(current_charts)
