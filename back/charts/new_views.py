import cloudinary.uploader
from datetime import datetime
from .utils3 import *
from django.http import HttpResponse

# Upload CSV content to Cloudinary
from io import StringIO
from time import sleep
import requests
from django.shortcuts import render
from .models import Chart, Chart_disc
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date, timedelta
import csv
import os
import json
from django.shortcuts import render
from django.conf import settings


def get_size(content):
    return len(content.getvalue()) / (1024 * 1024)


# Define a maximum size for each file (e.g., 10MB)
MAX_SIZE = 10


def chunk_dataframe(df):
    # Start by splitting the dataframe into two equal parts
    mid_idx = len(df) // 2
    chunks = [df.iloc[:mid_idx], df.iloc[mid_idx:]]

    new_chunks = []
    for chunk in chunks:
        csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
        sio = StringIO(csv_content)

        # If content is larger than MAX_SIZE, divide chunk into two again
        while get_size(sio) > MAX_SIZE:
            mid_idx = len(chunk) // 2
            new_chunks.extend([chunk.iloc[:mid_idx], chunk.iloc[mid_idx:]])
            chunk = new_chunks[-1]

            csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            sio = StringIO(csv_content)
        else:
            new_chunks.append(chunk)

    return new_chunks


class Updatefire(APIView):
    @staticmethod
    def get(req):

  
        # Read the JSON file and convert it into a dictionary
        with open(json_file_path, "r") as json_file:
            loaded_data = json.load(json_file)


        
  
        #global loaded_data
        master = []
        for tag in [
            "hardstyle",
            "tekkno",
            "techno",
            "drill",
            "hardtekk",
            "tekk",
            "rap techno",
            "phonk",
            "lofi",
            "lo-fi",
            "tiktok",
            "sped-up",
            "spedup",
            "slowed",
            "remix",
            "viral",
            "sad",
            "tired",
            "rage",
            "gym",
            "pump",
            "zyzz",
            "fuark",
            "zyzzcore",
            "breakcore",
            "corecore",
            "stutterhouse"
        ]:
            # tag = "hardstyle"
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

            response = requests.get(
                f"https://api-v2.soundcloud.com/search/tracks?q=*&filter.genre_or_tag={tag}&sort=popular&client_id=iZIs9mchVcX5lhVRyQGGAYlNPVldzAoX&limit=500&offset=0&linked_partitioning=1&app_version=1689322736&app_locale=en",
                headers=headers,
            )
            dt = response.json()

            dawn = pd.DataFrame(dt["collection"])
            dawn["tags"] = tag
            today = datetime.today().strftime("%Y-%m-%d")
            dawn["Date"] = today
            master.append(dawn)

        dawn = pd.concat(master)
        print(dawn.shape)

        columns = [
            "tags",
            "title",
            "likes_count",
            "playback_count",
            "reposts_count",
            "release_date",
            "Date",
            "artwork_url",
            "permalink_url",
            "uri"
        ]

        din = dawn[columns]
        din.columns

        din["uri"] = din["uri"].str.lstrip("https://api.soundcloud.com/tracks/")

        # Apply the function to the columns and create a new column
        gt = din.apply(
            lambda row: book(row["title"], row["tags"], row["permalink_url"],row["uri"]), axis=1
        )

        blake = pd.DataFrame(gt.to_list())

        print(blake.columns)
        print(blake.shape)

        din[
            [
                "spotify_name",
                "spotify_url",
                "competitor_track",
                "competitor",
                "comp_url",
            ]
        ] = blake
        din[
            [
                "spotify_name",
                "spotify_url",
                "competitor_track",
                "competitor",
                "comp_url",
            ]
        ]
        din = din.reset_index()

        din["index"] = din["index"] + 1
        din = din.rename(
            columns={
                "index": "curr_position",
                "likes_count": "likes",
                "play_count": "play",
                "reposts_count": "repost",
                "release_date": "release",
                "artwork_url": "thumbnail_url",
                "permalink_url": "soundcloud_link",
            }
        )
        din[["author_name", "author_url", "html"]] = ""

        din = din.drop(columns=["uri"])
        # Get today's date
        today = date.today()
        file_name = f"top300/{today}_a.csv"

        csv_content = din.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
        result = cloudinary.uploader.upload(
            StringIO(csv_content),
            public_id=file_name,
            folder="/Soundcloud/",
            resource_type="raw",
            overwrite=True,
        )
        
        # Saving dictionary to JSON file
        save_data()

        # Assuming loaded_data is your original dictionary
        split_data = split_dict_equally(loaded_data, 3)

        suffixes = ["_a", "_b", "_c"]
       

        for i, data in enumerate(split_data):
            json_str = json.dumps(data)
            encoded_data = json_str.encode('utf-8')
            result = cloudinary.uploader.upload(
                encoded_data,
                public_id=f"loaded_data{suffixes[i]}.json",
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )


        return Response(
            {
                "status": "success",
            },
            status=201,
        )


music_types = [
    "all-music",
    "trap",
    "ambient",
    "latin",
    "jazzblues",
    "deephouse",
    "pop",
    "reggae",
    "rock",
    "dancehall",
    "triphop",
    "classical",
    "dubstep",
    "rbsoul",
    "soundtrack",
    "electronic",
    "metal",
    "reggaeton",
    "disco",
    "hiphoprap",
    "house",
    "techno",
    "indie",
    "piano",
    "trance",
    "country",
    "alternativerock",
    "world",
    "danceedm",
    "folksingersongwriter",
    "drumbass",
]


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.1",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "OAuth 2-294078-444389085-iIl21X0gbFjMWd",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://soundcloud.com",
    "Referer": "https://soundcloud.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/115.0.0.0",
}

params = {
    "ids": "1056989302,1051523650,111127967,115236819,1194533935,1204457869,1242757588,1247116825,1263196699,1267447333,1269345835,1273484212,1275853348,1301428681,1339623658,1389272428,1393753888,1418341354,1428974836,1436403271,1436403670,1441741387,1443741343,1449523786,1454585971,1459277209,1459277581,1459277827,1459278433,1459278556,1459278877,1459279579,1460303899,1485545800,1491677641,1520926177,180905489,247837953,253006715,383244017,646736838,665261066,673254992,709649923,887243206,887244826,894055741,930408532,959334589,959336380",
    "client_id": "MK6Otkm10RJQcH3Cju78UhH6NXw40V47",
    "[object Object]": "",
    "app_version": "1690193099",
    "app_locale": "en",
}


class Discoverfire(APIView):
    @staticmethod
    def get(req):


        # Read the JSON file and convert it into a dictionary
        with open(json_file_path, "r") as json_file:
            loaded_data = json.load(json_file)


        master = []
        for country, co in [
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
        ]:
            print(co)
            for typex in music_types[:]:
                try:

                    url = (
                        f"https://soundcloud.com/discover/sets/charts-top:{typex}:{co}"
                    )

                    dummy = extract_dictionary_from_html(url)
                    sleep(5)
                    ids_to_sort_by = [int(i) for i in dummy]
                    # Sort the new_ids_list alphabetically
                    dummy.sort()

                    # Convert the sorted list back to a string with comma separation
                    new_ids_str = ",".join(dummy)

                    # Format the params dictionary with the new sorted ids
                    params_formatted = params.copy()
                    params_formatted["ids"] = new_ids_str

                    response = requests.get(
                        "https://api-v2.soundcloud.com/tracks",
                        params=params_formatted,
                        headers=headers,
                    )

                    dt = response.json()
                    # print(dt)

                    sorted_data = sorted(
                        dt, key=lambda x: ids_to_sort_by.index(x["id"])
                    )

                    dawn = pd.DataFrame(sorted_data)

                    dawn["tags"] = typex
                    dawn["country"] = country
                    dawn["Date"] = date.today()
                    master.append(dawn)
                except:
                    print(f"skipping ,{co},{typex}")

                    pass

        dawn = pd.concat(master)
  

        columns = [
            "tags",
            "country",
            "title",
            "likes_count",
            "playback_count",
            "reposts_count",
            "release_date",
            "Date",
            "artwork_url",
            "permalink_url",
            "uri"
        ]

        din = dawn[columns]
        din.columns

        din["uri"] = din["uri"].str.lstrip("https://api.soundcloud.com/tracks/")
        # Apply the function to the columns and create a new column
        gt = din.apply(
            lambda row: book(row["title"], row["tags"], row["permalink_url"],row["uri"]), axis=1
        )

        din[
            [
                "spotify_name",
                "spotify_url",
                "competitor_track",
                "competitor",
                "comp_url",
            ]
        ] = pd.DataFrame(gt.to_list())

        din = din.reset_index()

        din["index"] = din["index"] + 1
        din = din.rename(
            columns={
                "index": "curr_position",
                "likes_count": "likes",
                "play_count": "play",
                "reposts_count": "repost",
                "release_date": "release",
                "artwork_url": "thumbnail_url",
                "permalink_url": "soundcloud_link",
            }
        )
        din[["author_name", "author_url", "html"]] = ""
        

        din = din.drop(columns=["uri"])

        # Get today's date
        today = date.today()
        base_file_name = f"top50/{today}.csv"
        chunks = chunk_dataframe(din)

        for index, chunk in enumerate(chunks):
            csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            sio = StringIO(csv_content)

            suffix = chr(97 + index)  # 97 is ASCII for 'a'
            # file_name = f"{base_file_name}_{suffix}.csv"
            file_name = f"top50/{today}_{suffix}.csv"

            result = cloudinary.uploader.upload(
                sio,
                public_id=file_name,
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )

        # Saving dictionary to JSON file
        save_data()

        # Assuming loaded_data is your original dictionary
        split_data = split_dict_equally(loaded_data, 3)

        suffixes = ["_a", "_b", "_c"]
       

        for i, data in enumerate(split_data):
            json_str = json.dumps(data)
            encoded_data = json_str.encode('utf-8')
            result = cloudinary.uploader.upload(
                encoded_data,
                public_id=f"loaded_data{suffixes[i]}.json",
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )

        return Response(
            {
                "status": "success",
            },
            status=201,
        )


def download_file(request):
    folder = request.GET.get("folder")
    filename = request.GET.get("filename") + ".csv"
    # Construct the options dictionary

    if folder and filename:
        public_id = f"Soundcloud/{folder}/{filename}"
        # file_url = f"https://res.cloudinary.com/dfduoxw3q/raw/upload/v1693070034/{public_id}"
        file_url = cloudinary.utils.cloudinary_url(public_id, resource_type="raw")[0]
        print(file_url)
        response = HttpResponse(content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={filename}"

        # Fetch the file content
        import requests

        file_content = requests.get(file_url).content
        response.write(file_content)

        return response
    else:
        return HttpResponse("Invalid parameters provided.")





class Updatefir(APIView):
    @staticmethod
    def get(req):

        # Read the JSON file and convert it into a dictionary
        with open(json_file_path, "r") as json_file:
            loaded_data = json.load(json_file)

        print(len(loaded_data.keys()))

        import requests

        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }


        for key in list(loaded_data.keys())[:] :
            try:
                #print(loaded_data[key])
                loaded_data[key]["uri"]
                print("got")
            except:

                response = requests.get(f'{key}', headers=headers)
                script_content  =  response.text

                import re

                script_content
                match = re.search(r'"id":(\d+),"kind":"track"', script_content)
                if match:
                    trackid = match.group(1)
                    print(trackid)  # Output: 1590780219
                else:
                    print("Track ID not found!")
                    trackid = None

                loaded_data[key]["uri"] = trackid
            

        # Saving dictionary to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(loaded_data, json_file, indent=4)

        return Response(
            {
                "status": "success",
            },
            status=201,
        )




class Keywords(APIView):
    @staticmethod
    def get(req):

        pan = []
        countries = ["DE", "GB", "US", "NL", "FR", "AU", "BR", "PL", "SE", "AT", "IN", "CA", "TR", "CH", "NO", "ID", "MX"]


        for opd,query in output_pairs[:]:
            for cd in countries :
                if not query:
                    query = opd.lower()
                query = query.replace("-","")
                result = search_spotify_albums_country(query,cd, client_ids, client_secrets, max_attempts=8)
                bako = pd.DataFrame(result["tracks"]["items"])
                bako = bako.reset_index()
                bako["country"] = cd
                bako["keyword"] = query
                bako["target_track"] = opd
                pan.append(bako)


        book = pd.concat(pan)

        look = book[['index', 'album',  'duration_ms',
        'href', 'id',
        'name', 'popularity',  'country', 'keyword', 'target_track']]
        

        look["artist"] = book.album.apply(lambda x : x["artists"][0]["name"])

        look["artist_url"] = book.album.apply(lambda x : x["artists"][0]["href"])

        look["duration"]  =  look.duration_ms.apply(convert_ms_to_mm_ss)

        look = look[['country', 'keyword', 'target_track', 'index',  'duration', 'href', 'id', 'name', 'popularity',
                'artist', 'artist_url']]

        look["index"] = look["index"] + 1

        look = look.rename(columns ={"index":"position"})

        from datetime import date

        look["Date"] = date.today() 

        # Get today's date
        today = date.today()

        base_file_name = f"keywords/{today}.csv"
        chunks = chunk_dataframe(look)

        for index, chunk in enumerate(chunks):
            csv_content = chunk.to_csv(index=False, quoting=csv.QUOTE_ALL, sep="|")
            sio = StringIO(csv_content)

            suffix = chr(97 + index)  # 97 is ASCII for 'a'
            # file_name = f"{base_file_name}_{suffix}.csv"
            file_name = f"keywords/{today}_{suffix}.csv"

            result = cloudinary.uploader.upload(
                sio,
                public_id=file_name,
                folder="/Soundcloud/",
                resource_type="raw",
                overwrite=True,
            )


        return Response(
            {
                "status": "success",
            },
            status=201,
        )