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
            # -------------------------- 画像編集処理 --------------------------
            data = form.save(commit=False) # フォームデータの取得
            upload_img = request.FILES["stamp_image"]
            img = Image.open(upload_img).convert("RGB")
            img = img.filter(ImageFilter.BLUR) # ぼかし
            img = img.filter(ImageFilter.SHARPEN) # シャープ
            img = img.convert("L") # グレースケール
            img = img.filter(ImageFilter.EDGE_ENHANCE) # エッジ強調
            # セピア化
            Image.merge(
                mode="RGB",
                bands=(
                    img.point(lambda x: x * 240 / 255),
                    img.point(lambda x: x * 200 / 255),
                    img.point(lambda x: x * 145 / 255)
                )
            )

            # -------------------------- データ追加処理 --------------------------
            buffer = io.BytesIO()
            img.save(buffer, format=img.format or "JPEG")
            buffer.seek(0)
            data.stamp_image.save(upload_img.name, ContentFile(buffer.read()), save=False)
            data.save()
            return redirect("home")
    else:
        form = StampPinForm()
    context["form"] = form
    return render(request, template_name, context)

