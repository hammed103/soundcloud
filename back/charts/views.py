from django.shortcuts import render
from .models import Chart, Chart_disc
import requests
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from pyairtable import Api, Base, Table
import re
import pyairtable


api_key = "keyPTU7Oyav6HW5aK"
base_id = "appAcwKKL0mqVM14s"
table_name = "Tiktok"


airtable = pyairtable.Table(api_key, base_id, table_name)

"""from django.db.models import Count

# Step 1: Identify the duplicate entries (based on song title and tags)
duplicate_songs = (
    Chart.objects.values("title", "tags")
    .annotate(count=Count("id"))
    .filter(count__gt=1)
)

# Step 2: Decide which entry to keep (let's assume we keep the one with the highest ID)
for entry in duplicate_songs:
    song_title = entry["title"]
    song_tags = entry["tags"]
    # Get the duplicate entries with the same title and tags
    duplicate_entries = Chart.objects.filter(title=song_title, tags=song_tags)

    # Decide which entry to keep (e.g., the one with the highest ID)
    entry_to_keep = duplicate_entries.order_by("-id").first()

    # Step 3: Delete the duplicate entries (excluding the one we decided to keep)
    duplicate_entries.exclude(id=entry_to_keep.id).delete()"""


@csrf_exempt
def tiktok_view(request):
    if request.method == "POST":
        # Get the TikTok URL from the POST request
        tiktok_url = request.POST.get("url", "")

        # Validate the TikTok URL (you may add more robust validation here)
        if not tiktok_url.startswith("https://www.tiktok.com/"):
            return JsonResponse({"error": "Invalid TikTok URL"})

        # Prepare the JSON data for the API request
        data = {"url": tiktok_url}

        # Make a POST request to the specified endpoint (you may adjust the URL as needed)
        api_endpoint = "http://167.99.195.35/api/tik"
        try:
            response = requests.post(api_endpoint, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            api_response = response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Error making the API request"})

        return JsonResponse(api_response)

    return render(request, "tiktok_form.html")


def extract_tiktok_username(url):
    # Split the URL using the '/' character
    parts = url.split("/")

    # Find the part of the URL containing '@' followed by the username
    for part in parts:
        if part.startswith("@"):
            return part

    # If no '@' symbol followed by username is found, return None
    return None


def loader(url):

    url = f"{url}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    tiktok_username = extract_tiktok_username(response.url)
    if tiktok_username is None:
        user_info = None
        return user_info
    url = f"https://www.tiktok.com/{tiktok_username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extracting the profile/bio information from the HTML
        user_info = {}
        user_info["username"] = tiktok_username
        nm = soup.find("div", class_=re.compile(r"DivShareTitleContainer"))
        try:
            user_info["title"] = nm.find("h1").text
        except:
            user_info["title"] = ""
            user_info = None
            return user_info
        try:
            user_info["subtitle"] = nm.find("h2").text
        except:
            user_info["subtitle"] = ""
        inf = soup.find("div", class_=re.compile(r"DivShareLayoutHeader"))
        try:
            user_info["followers"] = inf.find_all("strong")[1].text
        except:
            user_info["followers"] = ""
        try:
            user_info["following"] = inf.find_all("strong")[0].text
        except:
            user_info["following"] = ""
        try:
            user_info["likes"] = inf.find_all("strong")[2].text
        except:
            user_info["likes"] = ""
        try:
            user_info["image"] = inf.find("img")["src"]
        except:
            user_info["image"] = ""
        try:
            user_info["bio"] = soup.find("h2", class_=re.compile(r"H2ShareDesc")).text
        except:
            user_info["bio"] = "No Bio Yet"
        try:
            user_info["external_link"] = soup.find(
                "div", class_=re.compile(r"DivShareLinks")
            ).text
        except:
            user_info["external_link"] = ""

    return user_info


from datetime import date, timedelta

today = date.today() - timedelta(1)


def generate_top_50(current_chart, today):
    # Get the previous top 50 chart from yesterday
    yesterday = today - timedelta(days=1)

    # Create new entries for today's chart and update position_7_days_ago
    for i, song in enumerate(current_chart, start=1):
        song_tags = song["tags"]
        song_title = song["title"]
        curr_pos = song["current_position"]
        sound_play = song["sound_play"]
        sound_likes = song["sound_likes"]
        sound_repost = song["sound_repost"]
        sound_release = song["sound_release"]
        link = song["link"]

        # Check if the song with the same title and tags already exists in the database for today's chart
        existing_chart_obj = Chart.objects.filter(
            title=song_title, tags=song_tags, today=today
        ).first()

        if existing_chart_obj:
            # Song with the same title and tags already exists for today's chart, do nothing
            pass
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
            try:
                prev_pos, _ = (
                    Chart.objects.filter(
                        title=song_title, tags=song_tags, today=yesterday
                    )
                    .values_list("current_position", "previous_position")
                    .first()
                )
            except:
                prev_pos = None
            chart_obj = Chart(
                title=song_title,
                previous_position=prev_pos,
                current_position=curr_pos,
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
                today=today,
            )
            chart_obj.save()
            # Set position_7_days_ago for the new entry
            seven_days_ago = today - timedelta(days=7)
            try:
                print(song_title, song_tags, seven_days_ago)
                song_7_days_ago = Chart.objects.get(
                    title=song_title,
                    tags=song_tags,
                    today=seven_days_ago,
                )
                new_entry = Chart.objects.get(
                    title=song_title, tags=song_tags, today=today
                )
                new_entry.position_7_days_ago = song_7_days_ago.current_position
                new_entry.save()
            except Chart.DoesNotExist:
                new_entry = Chart.objects.get(
                    title=song_title, tags=song_tags, today=today
                )
                new_entry.position_7_days_ago = None
                new_entry.save()


def generate_discover(current_chart, today):
    # Get the previous top 50 chart from yesterday
    yesterday = today - timedelta(days=1)

    # Create new entries for today's chart and update position_7_days_ago
    for i, song in enumerate(current_chart, start=1):
        song_tags = song["tags"]
        song_title = song["title"]
        country = song["country"]
        curr_pos = song["current_position"]
        sound_play = song["sound_play"]
        sound_likes = song["sound_likes"]
        sound_repost = song["sound_repost"]
        sound_release = song["sound_release"]
        link = song["link"]

        # Check if the song with the same title and tags already exists in the database for today's chart
        existing_chart_obj = Chart_disc.objects.filter(
            title=song_title, tags=song_tags, today=today
        ).first()

        if existing_chart_obj:
            # Song with the same title and tags already exists for today's chart, do nothing
            pass
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
            try:
                prev_pos, _ = (
                    Chart_disc.objects.filter(
                        title=song_title, tags=song_tags, today=yesterday
                    )
                    .values_list("current_position", "previous_position")
                    .first()
                )
            except:
                prev_pos = None
            chart_obj = Chart_disc(
                title=song_title,
                previous_position=prev_pos,
                current_position=curr_pos,
                country=country,
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
                today=today,
            )
            chart_obj.save()
            # Set position_7_days_ago for the new entry
            seven_days_ago = today - timedelta(days=7)
            try:
                song_7_days_ago = Chart_disc.objects.get(
                    title=song_title,
                    tags=song_tags,
                    today=seven_days_ago,
                )
                new_entry = Chart_disc.objects.get(
                    title=song_title, tags=song_tags, today=today
                )
                new_entry.position_7_days_ago = song_7_days_ago.current_position
                new_entry.save()
            except Chart_disc.DoesNotExist:
                new_entry = Chart_disc.objects.get(
                    title=song_title, tags=song_tags, today=today
                )
                new_entry.position_7_days_ago = None
                new_entry.save()


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


class RenderDiscovery(APIView):
    @staticmethod
    def get(request):

        # tags = request.data["tags"]
        previous_chart = Chart_disc.objects.order_by("current_position")

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

        result = loader(request.data["url"])
        if result:
            airtable.create(result)
            print(result)
            return Response(
                {
                    "status": "success",
                    "data": result,
                },
                status=201,
            )
        else:
            print(result)
            return Response(
                {
                    "status": "Failed",
                    "data": "No profile found",
                },
                status=201,
            )


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

        generate_top_50(current_charts, today=today)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )


class Discover(APIView):
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
        params = {
            "ids": "1051523650,1056989302,111127967,115236819,1194533935,1204457869,1242757588,1247116825,1263196699,1267447333,1269345835,1273484212,1275853348,1301428681,1339623658,1389272428,1393753888,1418341354,1428974836,1436403271,1436403670,1441741387,1443741343,1449523786,1454585971,1459277209,1459277581,1459277827,1459278433,1459278556,1459278877,1459279579,1460303899,1485545800,1491677641,1520926177,180905489,247837953,253006715,255790653,383244017,646736838,665261066,673254992,709649923,887243206,894055741,930408532,959334589,959336380",
            "client_id": "MK6Otkm10RJQcH3Cju78UhH6NXw40V47",
            "[object Object]": "",
            "app_version": "1690193099",
            "app_locale": "en",
        }

        response = requests.get(
            "https://api-v2.soundcloud.com/tracks", params=params, headers=headers
        )
        dt = response.json()
        current_chart = [
            {
                "tags": "top-charts",
                "country": "us",
                "current_position": index + 1,
                "title": i["title"],
                "link": i["permalink_url"],
                "sound_likes": i["likes_count"],
                "sound_play": i["playback_count"],
                "sound_repost": i["reposts_count"],
                "sound_release": i["display_date"],
            }
            for index, i in enumerate(response.json())
        ]

        generate_discover(current_chart, today=today)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )
