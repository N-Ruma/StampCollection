from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("add_stamp_pin", add_stamp_pin_view, name="add_stamp_pin"),
    path("mypage", mypage_view, name="mypage"), 
    path("test_js", test_js_view, name="test_js"),
    path("map_view", map_view, name="map_view"),
    path("stamp_list", stamp_list_view, name="stamp_list"),
    path("get_stamp", get_stamp_view, name="get_stamp"),
    path("stamp/<int:stamp_id>", stamp_detail_view, name="stamp_detail")
]