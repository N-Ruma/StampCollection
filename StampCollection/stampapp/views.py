from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import MapPin
from .forms import MapPinForm

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

def home_view(request):
    template_name = "stampapp/home_view.html"
    context = {}
    return render(request, template_name, context)

@login_required
def add_map_pin_view(request):
    template_name = "stampapp/add_map_pin_view.html"
    context = {}
    if request.method == "POST":
        form = MapPinForm(request.POST)
        if form.is_valid():
            # formからデータを受け取り，MapPinを追加する
            map_pin = MapPin()
            map_pin.name = form.cleaned_data.get("name") # type: ignore
            map_pin.latitude = form.cleaned_data.get("latitude") # type: ignore
            map_pin.longitude = form.cleaned_data.get("longitude") # type: ignore
            map_pin.save()
            return redirect("home")
    else:
        form = MapPinForm()
    context["form"] = form
    return render(request, template_name, context)
