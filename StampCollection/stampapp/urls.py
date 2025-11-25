from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("add_map_pin", views.add_map_pin_view, name="add_map_pin"),
]