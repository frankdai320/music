"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
import djangae
from django.contrib import admin
from django.utils import six

if django.VERSION[0] == 1:
    from django.conf.urls import include, url
else:
    from django.urls import include, re_path as url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^_ah/', include('djangae.urls')),
    url(r'^', include('music_app.urls'))
]
