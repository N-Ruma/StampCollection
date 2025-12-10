from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image, ImageFilter, ImageOps
import io

from .models import *
from .forms import *

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

# @login_required
# def get_stamp_view(request):
#     template_name = "stampapp/get_stamp.html"
#     context = {}
#     user = request.user
#     if request.method == "POST":
#         id = request.POST.get("id")
#         try:
#             stamp = StampPin.objects.get(id=id)
#         except StampPin.DoesNotExist as e:
#             context["error"] = f"{e}"
#         else:
#             stamp.users.add(user)
#             context["message"] = "You Got Stamp!"

#     stamps = StampPin.objects.all()
#     context["stamps"] = stamps

#     own_stamps = user.stamppin_set.all() # type: ignore
#     context["own_stamps"] = own_stamps
#     return render(request, template_name, context)

THRESHOLD = 0.80 
#@login_required 
def stamp_detail_view(request, stamp_id): 
    stamp = StampPin.objects.get(id=stamp_id) 
    similarity = None 
    # ユーザーがこのスタンプを既に持っているか？ 
    user_has_stamp = UserStampPin.objects.filter( user=request.user, stamp=stamp ).exists() 
    # POST かつ 未所持 のときアップロード判定 
    if request.method == "POST" and not user_has_stamp: 
      img = request.FILES["upload_image"] 
    # 一時保存 
    path_uploaded = default_storage.save(f"tmp/{img.name}", img) 
    abs_uploaded = default_storage.path(path_uploaded) 
    # 基準画像（必要なら後で修正） 
    base_image_path = os.path.join( settings.BASE_DIR, "stampapp", "static", "stampapp", "base", "hakutyou1.jpg" )
    # 類似度判定 
    similarity = calculate_similarity(abs_uploaded, base_image_path) 
    if similarity >= THRESHOLD: 
      UserStampPin.objects.create(user=request.user, stamp=stamp) 
      return redirect("stamp_get", stamp_id=stamp.id) 
    return render( request, "stampapp/detail.html", { "stamp": stamp, "user_has_stamp": False, "similarity": similarity, "error": "残念…もう一度挑戦してね！", } ) 
    # GET あるいは既に取得済み 
    return render( request, "stampapp/detail.html", { "stamp": stamp, "user_has_stamp": user_has_stamp, } ) 

#@login_required 
def get_stamp_view(request, stamp_id): 
    stamp_pin = StampPin.objects.get(id=stamp_id) 
    stamp = stamp_pin.stamp 
    return render( request, "stampapp/get_stamp.html", {"stamp": stamp} )