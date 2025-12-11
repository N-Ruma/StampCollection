from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from PIL import Image, ImageFilter, ImageOps

from .models import *
from .forms import *

from .judge import judge

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

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

THRESHOLD = 0.80 
@login_required
def stamp_detail_view(request, stamp):
    template_name = "stampapp/stamp_detail.html"
    context = {}

    user = request.user
    own_stamp = StampPin.objects.filter(name=stamp, users=user).first()
    unknown_stamp = StampPin.objects.get(name=stamp)
    
    if own_stamp:
        context["own_stamp"] = own_stamp
    else:
        context["unknown_stamp"] = unknown_stamp
    
    return render(request, template_name, context)

def judge_view(request):
    template_name = "stampapp/judge.html"
    context = {}

    user = request.user
    messages = []

    # POSTリクエストは獲得処理を行いたいとき(スタンプ未獲得時)にのみ発生するはずなので，現段階でのバグ対策は割愛 (2025/12/11)
    if request.method == "POST":
        stamp = request.POST["stamp"]
        unknown_stamp = StampPin.objects.get(name=stamp)
        upload_image = request.FILES["upload_image"]

        if judge(unknown_stamp.stamp_image, upload_image):
            unknown_stamp.users.add(user)
            success_message = f"{unknown_stamp}を獲得しました!"
            messages.append(success_message)
            context["stamp"] = unknown_stamp
        else:
            failed_message = "スタンプを獲得できませんでした. 別の画像を試してください!"
            messages.append(failed_message)
        
    context["messages"] = messages
    return render(request, template_name, context)