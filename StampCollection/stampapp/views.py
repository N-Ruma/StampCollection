from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import StampPin
from .forms import StampPinForm

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

def home_view(request):
    template_name = "stampapp/home_view.html"
    context = {}
    return render(request, template_name, context)

@login_required
def add_stamp_pin_view(request):
    template_name = "stampapp/add_stamp_pin_view.html"
    context = {}
    if request.method == "POST":
        form = StampPinForm(request.POST, request.FILES)
        if form.is_valid():
            # formからデータを受け取り，MapPinを追加する
            # stamp_pin = StampPin()
            # stamp_pin.name = form.cleaned_data.get("name") # type: ignore
            # stamp_pin.latitude = form.cleaned_data.get("latitude") # type: ignore
            # stamp_pin.longitude = form.cleaned_data.get("longitude") # type: ignore
            # stamp_pin.stamp_image = request.FILES.get("stamp_image")
            # stamp_pin.save()
            form.save()
            return redirect("home")
    else:
        form = StampPinForm()
    context["form"] = form
    return render(request, template_name, context)
