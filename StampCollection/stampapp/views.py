import math
from django.shortcuts import render, redirect
from django.db.models import Case,When,Value,IntegerField
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import *
from .forms import *
from .judge import *

# 設定されている認証ユーザモデルを取得する.
User = get_user_model()

# 距離条件用追加コード,judge_viewで使う
def calc_distance(lat1, lng1, lat2, lng2):
    R = 6371000  # 地球半径(m)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def home_view(request):
    template_name = "stampapp/home.html"
    context = {}

    popular_stamps = (
        StampPin.objects.annotate(user_count=Count("users"))
        .filter(user_count__gt=0)   #user_count が 0 より大きいものだけを取得する ← 追加：0人は除外
        .order_by("-user_count")[:3]
    )
    context["popular_stamps"] = popular_stamps
    return render(request, template_name, context)


@login_required
def add_stamp_pin_view(request):
    template_name = "stampapp/add_stamp_pin.html"
    context = {}

    form = StampPinForm()
    context["form"] = form

    stamps = StampPin.objects.all()
    context["stamps"] = stamps

    return render(request, template_name, context)

def result_add_stamp_pin_view(request):
    template_name = "stampapp/result_add_stamp_pin.html"
    context = {}
    messages = []

    if request.method == "POST":
        form = StampPinForm(request.POST, request.FILES)
        if form.is_valid():
            stamp_image = form.cleaned_data["stamp_image"]
            exist_stamps = StampPin.objects.all()

            # 類似度[ threshold ]以上のスタンプが存在するかどうか
            threshold = 0.97
            if any(list(map(lambda stamp: judge(stamp.stamp_image, stamp_image, threshold), StampPin.objects.all()))):
                messages.append("類似度の高いスタンプ画像を持つスタンプが既に追加されています.")
            else:
                form.save()
                messages.append("スタンプを追加しました!")

    context["messages"] = messages
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

    user = request.user
    s = int(request.GET.get("s", 0))

    # --- マップ用（全件・順序不要） ---
    map_stamps = StampPin.objects.all()

    # --- 一覧用（ソート対象） ---
    list_stamps = StampPin.objects.all().prefetch_related("users")

    if s == 1:
        list_stamps = list_stamps.order_by("name")

    elif s == 2:
        list_stamps = list_stamps.order_by("-name")

    elif s == 3:
        # 獲得済みを上に
        list_stamps = list_stamps.annotate(
            got_order=Case(
                When(users=user, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by("got_order", "name")

    elif s == 4:
        # 未獲得を上に
        list_stamps = list_stamps.annotate(
            got_order=Case(
                When(users=user, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by("got_order", "name")

    context = {
        "stamps": map_stamps, # マップ用
        "list_stamps": list_stamps, # 一覧用
        "current_sort": s,
    }

    return render(request, template_name, context)

@login_required
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

    if request.method == "POST":

        stamp_name = request.POST.get("stamp")
        user_lat = request.POST.get("user_lat")
        user_lng = request.POST.get("user_lng")
        upload_image = request.FILES.get("upload_image")

        # 必須データが欠けている場合
        if not stamp_name or not user_lat or not user_lng or not upload_image:
            messages.append("必要な情報が取得できませんでした。位置情報を許可してください。")
            context["messages"] = messages
            return render(request, template_name, context)

        unknown_stamp = StampPin.objects.get(name=stamp_name)

        user_lat = float(user_lat)
        user_lng = float(user_lng)

        distance = calc_distance(
            user_lat, user_lng,
            unknown_stamp.latitude,
            unknown_stamp.longitude
        )

        if distance > 50:
            messages.append("スタンプ設置場所の範囲外です。")
        elif not judge(unknown_stamp.stamp_image, upload_image):
            messages.append("画像が一致しませんでした。")
        else:
            unknown_stamp.users.add(user)
            messages.append(f"{unknown_stamp}を獲得しました！")
            context["stamp"] = unknown_stamp

    context["messages"] = messages
    return render(request, template_name, context)