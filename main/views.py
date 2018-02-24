from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import Music
import re
import requests

def index(request):
    return getm(request, 1)

def getm(request, musicid):
    try:
        entry = Music.objects.get(pk=musicid)
        return render(request, "get.html", {'id':musicid, 'url':entry.link, 'date':entry.date_added, 'name':entry.owner})
    except ObjectDoesNotExist:
        return render(request, "missing.html", {'id':musicid})

@csrf_exempt
def add(request):
    if request.method == "POST":
        regex = re.compile("(youtu\.be\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v)\/))([^\?&\"'>]+)")
        regex = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?")
        match = regex.match(request.POST['url'])
        print(request.POST)
        if not match:
           return HttpResponse(request.POST['url'] + " is not a valid video url", content_type='text/plain', status=400)
        else:
            id = match[1]
            valid = requests.get("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=" + id + "&format=json")
            if valid.status_code == 404:
                return HttpResponse(request.POST['url'] + " is not a valid youtube video", content_type="text/plain", status=400)
            else:
                m = Music(link=id, date_added=timezone.now(), owner=request.POST['name'])
                m.save()
                return HttpResponse(request.POST['url'] + "sucessfully added", content_type="text/plain")

    else:
        return render(request, 'add.html')


