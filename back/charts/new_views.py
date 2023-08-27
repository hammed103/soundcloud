import cloudinary.uploader
from datetime import datetime
from .utils3 import *
from django.http import HttpResponse
# Upload CSV content to Cloudinary
from io import StringIO


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



import os
import json
from django.shortcuts import render
from django.conf import settings



class Updatefire(APIView):
    @staticmethod
    def get(req):


        master = []
        for tag in [
            'hardstyle',
            'tekkno',
            'techno'
            'drill',
            'hardtekk',
            'tekk',
            'lofi',
            'lo-fi',
            'tiktok',
            'sped-up',
            'spedup',
            'slowed',
            'remix',
            'viral',
            'rap techno'
             ] :
            #tag = "hardstyle"
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
            today = datetime.today().strftime('%Y-%m-%d')
            dawn["Date"] = today
            master.append(dawn)

        dawn = pd.concat(master)




        columns = [
            "tags", "title",
        "likes_count", "playback_count", "reposts_count", "release_date", "Date",
            "artwork_url","permalink_url"
        ]

        din = dawn[columns]
        din.columns

        # Apply the function to the columns and create a new column
        gt = din.apply(lambda row: book(row["title"], row["tags"],row['permalink_url']), axis=1)

        blake = pd.DataFrame(gt.to_list())

        print(blake.columns)
        print(blake.shape)

        din[["spotify_name","spotify_url","competitor_track","competitor","comp_url"]] = blake
        din[["spotify_name","spotify_url","competitor_track","competitor","comp_url"]]
        din = din.reset_index()

        din["index"]  = din["index"] + 1
        din = din.rename(columns ={"index":"curr_position","likes_count":"likes","play_count":"play","reposts_count":"repost","release_date":"release",
                            "artwork_url":"thumbnail_url","permalink_url":"soundcloud_link"})
        din[["author_name","author_url","html"]] = ""
        # Get today's date
        today = date.today() - timedelta(1)
        file_name = f"top300/{today}.csv"
        csv_content = din.to_csv(index=False)
        result = cloudinary.uploader.upload(StringIO(csv_content), public_id=file_name,folder="/Soundcloud/",resource_type='raw',overwrite=True)


        # Saving dictionary to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(loaded_data, json_file, indent=4)


        return Response(
            {
                "status": "success",
            },
            status=201,
        )





def download_file(request):
    folder = request.GET.get('folder')
    filename = request.GET.get('filename') + ".csv"
            # Construct the options dictionary

    if folder and filename:
        public_id = f"Soundcloud/{folder}/{filename}"
        #file_url = f"https://res.cloudinary.com/dfduoxw3q/raw/upload/v1693070034/{public_id}"
        file_url = cloudinary.utils.cloudinary_url(public_id,resource_type="raw")[0]
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
