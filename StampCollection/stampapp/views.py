from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image, ImageFilter, ImageOps
import io

from .models import *
from .forms import *
from .models import StampPin #追加12/4

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

def home_view(request):
    template_name = "stampapp/home.html"
    context = {}
    return render(request, template_name, context)

@login_required
def add_stamp_pin_view(request):
    template_name = "stampapp/add_stamp_pin.html"
    context = {}
    if request.method == "POST":
        form = StampPinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = StampPinForm()
    context["form"] = form
    return render(request, template_name, context)

@login_required
def test_js_view(request):
    template_name = "stampapp/test_js.html"
    context = {}
    stamps = StampPin.objects.all()
    context["stamps"] = stamps
    return render(request, template_name, context)

@login_required
def stamp_list_view(request):
    stamps = StampPin.objects.all()
    return render(request, "stampapp/stamp_list.html", {"stamps": stamps})


def map_view(request):
    stamps = StampPin.objects.all()
    return render(request, "stampapp/map_view.html", {"stamps": stamps})

@login_required
def stamp_detail_view(request, stamp_id):
    stamp = StampPin.objects.get(id=stamp_id)
    template_name = "stampapp/stamp_detail.html"
    return render(request, template_name, {"stamp": stamp})

@login_required
def get_stamp_view(request):
    template_name = "stampapp/get_stamp.html"
    context = {}
    user = request.user
    if request.method == "POST":
        id = request.POST.get("id")
        try:
            stamp = StampPin.objects.get(id=id)
        except StampPin.DoesNotExist as e:
            context["error"] = f"{e}"
        else:
            stamp.users.add(user)
            context["message"] = "You Got Stamp!"

    stamps = StampPin.objects.all()
    context["stamps"] = stamps

    own_stamps = user.stamppin_set.all() # type: ignore
    context["own_stamps"] = own_stamps
    return render(request, template_name, context)

