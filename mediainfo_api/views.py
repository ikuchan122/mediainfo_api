from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from math import ceil
from pymediainfo import MediaInfo
import time
import requests
from requests.exceptions import Timeout

from io import BytesIO

from mediainfo_api.validator import valid_url


@require_http_methods(["GET", "POST"])
@csrf_exempt
def getVideoDimensions(request):
    # POST
    if request.method == 'POST':
        video = request.FILES['file']

    # GET
    if request.method == 'GET':
        # validate query string / url param
        query_dict = request.GET
        if not 'url' in query_dict:
            return JsonResponse({'ok': False, 'message': 'Enter a valid parameter.'})

        # extract video url from query string
        query_str = query_dict.urlencode(safe=':/?&=')
        url = query_str[query_str.index('url=')+4:]
        if not valid_url(url):
            return JsonResponse({'ok': False, 'message': 'Enter a valid URL.'})

        # fetch video
        try:
            video = BytesIO(requests.get(url, timeout=(3, 10)).content)
        except Timeout:
            return JsonResponse({'ok': False, 'message': 'Connection timeout when downloading the video.'})

    # call Mediainfo.parse()
    print('request received!')
    start = time.time()
    tracks = MediaInfo.parse(video).video_tracks
    height, width, duration = 0, 0, 0
    for track in tracks:
        if track.height > height:
            height = track.height
            width = track.width
            duration = ceil(track.duration / 1000)
    end = time.time()

    # return json response
    if height == 0 or width == 0:
        return JsonResponse({'ok': False, 'message': 'Enter a valid URL to a video file.'})

    responseData = {
        'ok': True,
        'duration': duration,
        'height': height,
        'width': width,
        'mediainfo_process_time': end - start,
        'message': 'Successful.'
    }
    return JsonResponse(responseData)
