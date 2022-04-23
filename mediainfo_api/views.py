from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from math import ceil
from pymediainfo import MediaInfo
import time

from mediainfo_api.validator import valid_url


@require_http_methods(["GET", "POST"])
@csrf_exempt
def getVideoDimensions(request):
    if request.method == 'GET':
        query_str = request.GET
        if not 'url' in query_str:
            return JsonResponse({'ok': False, 'message': 'Enter a valid parameter.'})
        url = query_str['url']
        if not valid_url(url):
            return JsonResponse({'ok': False, 'message': 'Enter a valid URL.'})
        video = url

    if request.method == 'POST':
        video = request.FILES['file']

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
