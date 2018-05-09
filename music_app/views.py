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
    if request.GET.get('musicid'):
        musicid = request.GET.get('musicid') or 1
        return redirect(reverse('get music', kwargs={'musicid': musicid}))
    return render(request, 'music_app/index.html')


def getm(request, musicid):
    if musicid == 0:
        musicid = 1
    entry = getitem(musicid)
    # entry might be None, handled in template
    return render(request, "music_app/get.html", {'id': musicid, 'entry': entry, 'domain': request.get_host(),
                                                  'shuffle': request.GET.get('shuffle', False)})


@csrf_exempt
def add(request):
    if request.method == "POST":
        regex = re.compile("https?://(?:www\.|m\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]*)")
        url = request.POST.get('url', '')
        match = regex.match(url)
        if not match:
            return HttpResponse(url + " is not a valid video url", content_type='text/plain',
                                status=400)
        else:
            id = match[1]
            valid = requests.get(
                "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + id + "&format=json")
            if valid.status_code != 200:
                return HttpResponse(url + " is not a valid youtube video", content_type="text/plain",
                                    status=400)
            else:
                m = Music(link=id, date_added=timezone.now(), added_by=request.POST.get('name', '')[:200])
                m.save()
                return JsonResponse({'id': Music.objects.count(), 'url': url,
                                     'link': reverse('get music', kwargs={'musicid': Music.objects.count()})})

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


def latest(request):
    return redirect(reverse('get music', kwargs={'musicid': latest_valid_music_num()}))


def random_valid_music_num():
    """Return a random number from the set of valid music numbers."""
    return randbelow(Music.objects.count()) + 1


def latest_valid_music_num():
    """Return the number of the latest valid music."""
    return Music.objects.count()


def random(request):
    if request.GET.get('shuffle', False):
        return redirect(reverse('get music', kwargs={'musicid': random_valid_music_num()}) + '?shuffle=true')
    return redirect(reverse('get music', kwargs={'musicid': random_valid_music_num()}))
