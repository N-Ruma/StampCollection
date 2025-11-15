from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("google_map/", views.google_map_view, name="google_map"),
    path("leafret_map/", views.leafret_map_view, name="leafret_map"),
]