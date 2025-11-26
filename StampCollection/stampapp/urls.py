from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("add_stamp_pin", views.add_stamp_pin_view, name="add_stamp_pin"),
]