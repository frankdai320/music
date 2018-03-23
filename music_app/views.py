import re

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Music


def index(request):
    return getm(request, 1)


def getm(request, musicid):
    if musicid == 0:
        musicid = 1
    entry = getitem(musicid)
    # entry might be None, handled in template
    return render(request, "music_app/get.html", {'id': musicid, 'entry': entry, 'domain': request.get_host()})


@csrf_exempt
def add(request):
    if request.method == "POST":
        regex = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?")
        match = regex.match(request.POST['url'])
        if not match:
            return HttpResponse(request.POST['url'] + " is not a valid video url", content_type='text/plain',
                                status=400)
        else:
            id = match[1]
            valid = requests.get(
                "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + id + "&format=json")
            if valid.status_code != 200:
                return HttpResponse(request.POST['url'] + " is not a valid youtube video", content_type="text/plain",
                                    status=400)
            else:
                m = Music(link=id, date_added=timezone.now(), added_by=request.POST['name'])
                m.save()
                return JsonResponse({'id': Music.objects.count(), 'url': request.POST['url']})

    else:
        return render(request, 'music_app/add.html')


def getitem(num):
    try:
        entry = Music.objects.all()[int(num) - 1]
    except IndexError:
        return None
    return entry


@csrf_exempt
def api(request, musicid):
    entry = getitem(musicid)
    if entry:
        return JsonResponse({"id": entry.link, "name": entry.added_by, "time": entry.date_added.timestamp()})
    return JsonResponse({}, status=404)


@csrf_exempt
def num(request):
    return HttpResponse(Music.objects.count(), content_type='text/plain')


@csrf_exempt
def latest(request):
    return getm(request, Music.objects.count())
