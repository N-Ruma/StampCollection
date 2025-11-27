from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("add_stamp_pin", add_stamp_pin_view, name="add_stamp_pin"),
]