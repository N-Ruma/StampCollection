from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
import random

from .models import *
from .forms import *
from .judge import *

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
    user = request.user

    # 現在ログインしているユーザーが獲得しているスタンプ
    own_stamps = StampPin.objects.filter(users=user)
    context["own_stamps"] = own_stamps

    # ビンゴ
    bingo, _created = Bingo.objects.get_or_create(user=user)
    if request.method == "POST":
        reset_flag = int(request.POST.get("bingo-reset", 0))
        print(reset_flag)
        if reset_flag == 1:
            bingo.reset()
            bingo.save()
    context["bingo"] = bingo.get_bingo_data()

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
    bingo, _created = Bingo.objects.get_or_create(user=user)

    # POSTリクエストは獲得処理を行いたいとき(スタンプ未獲得時)にのみ発生するはずなので，現段階でのバグ対策は割愛 (2025/12/11)
    if request.method == "POST":
        stamp = request.POST["stamp"]
        unknown_stamp = StampPin.objects.get(name=stamp)
        upload_image = request.FILES["upload_image"]

        if judge(unknown_stamp.stamp_image, upload_image):
            # スタンプ処理
            unknown_stamp.users.add(user)
            success_message = f"{unknown_stamp}を獲得しました!"
            messages.append(success_message)
            context["stamp"] = unknown_stamp
            
            # ビンゴ更新
            target_num = random.randint(0, 24)
            bingo.change_true(target_num)
            bingo.save()
            context["target_num"] = target_num
        else:
            failed_message = "スタンプを獲得できませんでした. 別の画像を試してください!"
            messages.append(failed_message)

    # ビンゴ
    context["bingo"] = bingo.get_bingo_data()
        
    context["messages"] = messages
    return render(request, template_name, context)