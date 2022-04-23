from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from math import ceil
from pymediainfo import MediaInfo
import time


@require_POST
@csrf_exempt
def getVideoDimensions(request):
    start = time.time()
    print('request received!')
    video = request.FILES['file']
    tracks = MediaInfo.parse(video).video_tracks
    height, width, duration = 0, 0, 0
    for track in tracks:
        if track.height > height:
            height = track.height
            width = track.width
            duration = ceil(track.duration / 1000)

    end = time.time()
    if height == 0 or width == 0:
        return JsonResponse({'ok': False})

    responseData = {
        'ok': True,
        'duration': duration,
        'height': height,
        'width': width,
        'mediainfo_process_time': end - start
    }
    return JsonResponse(responseData)
