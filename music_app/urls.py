import django
from django.utils import six

from . import views

if django.VERSION[0] == 1:
    from django.conf.urls import include, url
else:
    from django.urls import include, re_path as url

urlpatterns = [
    url(r'^api/(?P<musicid>\d+)/$', views.api, name="get music api"),
    url(r'^api/random/$', views.api_random, name='api random'),
    url(r'^api/latest/$', views.api_latest, name='api latest'),
    url(r'^api/$', views.num, name="get number"),
    url(r'^(?P<musicid>\d+)/$', views.getm, name="get music"),
    url(r'^add/$', views.add, name="add music"),
    url(r'^latest/$', views.latest, name="latest"),
    url(r'^random/$', views.random, name='random'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^all/$', views.all_, name='all'),
    url(r'^renumber/$', views.renumber, name='renumber'),
    url(r'^$', views.index, name='index')
]
