from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", home_view, name="home"),
    path("add_stamp_pin", add_stamp_pin_view, name="add_stamp_pin"),
    path("result_add_stamp_pin", result_add_stamp_pin_view, name="result_add_stamp_pin"),
    path("mypage", mypage_view, name="mypage"), 
    path("map", map_view, name="map"),
    path("stamp_list", stamp_list_view, name="stamp_list"),
    path("stamp/<str:stamp>", stamp_detail_view, name="stamp_detail"),
    path("judge", judge_view, name="judge")

]