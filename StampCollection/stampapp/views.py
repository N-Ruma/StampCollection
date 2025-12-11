from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import Count
from PIL import Image, ImageFilter, ImageOps
import io

from .models import *
from .forms import *

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

# ------------------ for debug -------------------
@login_required
def test_js_view(request):
    template_name = "stampapp/test_js.html"
    context = {}
    stamps = StampPin.objects.all()
    context["stamps"] = stamps
    return render(request, template_name, context)
# -----------------------------------------------

def home_view(request):
    template_name = "stampapp/home.html"
    context = {}

    popular_stamps = (
        StampPin.objects.annotate(user_count=Count("users"))
        .order_by("-user_count")[:3]
    )
    context["popular_stamps"] = popular_stamps
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

    stamps = StampPin.objects.all()
    context["stamps"] = stamps
    return render(request, template_name, context)

@login_required
def mypage_view(request):
    template_name = "stampapp/mypage.html"
    context = {}
    # 現在ログインしているユーザーが獲得しているスタンプ
    own_stamps = StampPin.objects.filter(users=request.user)
    context["own_stamps"] = own_stamps
    return render(request, template_name, context)
    
@login_required
def get_stamp_view(request):
    template_name = "stampapp/get_stamp.html"
    context = {}
    
    user = request.user
    message = None
    error = None

    if request.method == "POST":
        stamp_id = request.POST.get("id")
        try:
            stamp = StampPin.objects.get(id=stamp_id)
        except StampPin.DoesNotExist:
            error = "スタンプが存在しません。"
        else:
            # すでに獲得済みかチェック
            if user in stamp.users.all():
                message = f"{stamp} はすでに獲得済みです。"
            else:
                stamp.users.add(user)
                message = f"{stamp} を獲得しました！"

    # 全スタンプ一覧
    stamps = StampPin.objects.all()
    context["stamps"] = stamps
    
    # 自分の獲得スタンプ
    own_stamps = StampPin.objects.filter(users=user)
    context["own_stamps"] = own_stamps
    
    context["message"] = message
    context["error"] = error
    
    return render(request, template_name, context)
  
@login_required
def stamp_list_view(request):
    template_name = "stampapp/stamp_list.html"
    context = {}
    
    user = request.user

    own_stamps = StampPin.objects.filter(users=user)
    context["own_stamps"] = own_stamps
    
    unknown_stamps = StampPin.objects.exclude(users=user)
    context["unknown_stamps"] = unknown_stamps

    return render(request, template_name, context)

def map_view(request):
    template_name = "stampapp/map.html"
    context = {}
    
    stamps = StampPin.objects.all()
    context["stamps"] = stamps
    
    return render(request, template_name, context)

@login_required
def stamp_detail_view(request, stamp):
    template_name = "stampapp/stamp_detail.html"
    context = {}
    
    own_stamp = StampPin.objects.filter(name=stamp, users=request.user).first()
    unknown_stamp = StampPin.objects.get(name=stamp)
    if own_stamp:
        context["own_stamp"] = own_stamp
    else:
        context["unknown_stamp"] = unknown_stamp
    
    return render(request, template_name, context)
