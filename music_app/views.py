import re
from secrets import randbelow  # using this instead of random because it provides a better distribution

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
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
        return JsonResponse({"id": entry.link, "name": entry.added_by, "time": entry.date_added.timestamp(),
                             'num': musicid})
    return JsonResponse({}, status=404)


@csrf_exempt
def api_random(request):
    return redirect(reverse('get music api', kwargs={'musicid': random_valid_music_num()}))


@csrf_exempt
def api_latest(request):
    return redirect(reverse('get music api', kwargs={'musicid': latest_valid_music_num()}))


@csrf_exempt
def num(request):
    return HttpResponse(Music.objects.count(), content_type='text/plain')


@csrf_exempt
def latest(request):
    return redirect(reverse('get music', kwargs={'musicid': latest_valid_music_num()}))


def random_valid_music_num():
    """Return a random number from the set of valid music numbers."""
    return randbelow(Music.objects.count()) + 1


def latest_valid_music_num():
    """Return the number of the latest valid music."""
    return Music.objects.count()


@csrf_exempt
def random(request):
    return redirect(reverse('get music', kwargs={'musicid': random_valid_music_num()}))
