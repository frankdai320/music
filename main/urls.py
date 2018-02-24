from django.conf.urls import url
from . import views
urlpatterns = [
    url('^api/(?P<musicid>\d+)/', views.api, name="get music api"),
    url('^(?P<musicid>\d+)/$', views.getm, name="get music"),
    url('^add/$', views.add, name="add music"),
    url('^$', views.index,name='index')
]
