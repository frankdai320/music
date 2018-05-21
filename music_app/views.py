import re

import requests
from django.core.exceptions import ObjectDoesNotExist
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
    if int(musicid) == 0:
        return redirect(reverse('get music', kwargs={'musicid': 1}))
    entry = getitem(musicid)
    if entry:
        entry.update_title()  # called every 2 weeks at most
    # entry might be None, handled in template
    return render(request, "music_app/get.html", {'id': musicid, 'entry': entry, 'domain': request.get_host(),
                                                  'shuffle': request.GET.get('shuffle', False)})


def browse(request):
    items_per_page = 50
    page_num = int(request.GET.get('page', '1'))
    end_index = items_per_page * page_num + 1
    start_index = end_index - items_per_page
    entries = []
    for n in range(start_index, end_index):
        entry = getitem(n)
        if entry:
            entries.append(entry)
            if not entry.title:
                entry.update_title(force=True)
    return render(request, 'music_app/browse.html',
                  {'page_num': page_num, 'first_num': start_index, 'entries': entries, 'page_length': items_per_page})


def all_(request):
    entries = Music.objects.all().order_by('position')
    for entry in entries:
        if not entry.title:
            entry.update_title(force=True)
    return render(request, 'music_app/browse.html',
                  {'page_num': 1, 'first_num': 1, 'entries': entries, 'page_length': 0})  # 0 prevents a "next" button


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
            id = match.group(1)
            valid = requests.get(
                "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + id + "&format=json")
            if valid.status_code != 200:
                return HttpResponse(url + " is not a valid youtube video", content_type="text/plain",
                                    status=400)
            else:
                ip = request.META['REMOTE_ADDR']
                m = Music(link=id,
                          date_added=timezone.now(),
                          title_cache_time=timezone.now(),
                          added_by=request.POST.get('name', '')[:200],
                          ip=ip,
                          position=Music.objects.count() + 1,  # not saved yet
                          title=valid.json().get('title', ''))

                titl
                m.save()
                return JsonResponse({'id': Music.objects.count(), 'url': url,
                                     'link': reverse('get music', kwargs={'musicid': Music.objects.count()})})

    else:
        return render(request, 'music_app/add.html')

def renumber(request):
    music = Music.objects.all().order_by('date_added')
    for i,m in enumerate(music):
        m.position = i+1
        m.save()
    return HttpResponse(status=204)


def getitem(num):
    try:
        entry = Music.objects.get(position=int(num))
    except ObjectDoesNotExist:
        return None
    else:
        return entry


def api(request, musicid):
    entry = getitem(musicid)
    if entry:
        import time
        timestamp = int(time.mktime(entry.date_added.timetuple())+entry.date_added.microsecond/1000000.0)
        return JsonResponse({"id": entry.link, "name": entry.added_by, "time": timestamp,
                             'num': musicid})
    return JsonResponse({}, status=404)


def api_random(request):
    return redirect(reverse('get music api', kwargs={'musicid': random_valid_music_num()}))


def api_latest(request):
    return redirect(reverse('get music api', kwargs={'musicid': latest_valid_music_num()}))


def num(request):
    return HttpResponse(Music.objects.count(), content_type='text/plain')


def latest(request):
    return redirect(reverse('get music', kwargs={'musicid': latest_valid_music_num()}))


def random_valid_music_num():
    """Return a random number from the set of valid music numbers."""
    import random
    return random.randint(1, Music.objects.count())


def latest_valid_music_num():
    """Return the number of the latest valid music."""
    return Music.objects.count()


def random(request):
    if request.GET.get('shuffle', False):
        return redirect(reverse('get music', kwargs={'musicid': random_valid_music_num()}) + '?shuffle=true')
    return redirect(reverse('get music', kwargs={'musicid': random_valid_music_num()}))
