from django.urls import path

from . import views

urlpatterns = [
    path('api/<int:musicid>/', views.api, name="get music api"),
    path('api/', views.num, name="get number"),
    path('<int:musicid>/', views.getm, name="get music"),
    path('add/', views.add, name="add music"),
    path('latest/', views.latest, name="latest"),
    path('random/', views.random, name='random'),
    path('', views.index, name='index')
]
