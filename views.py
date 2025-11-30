from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import StampPin
from .forms import StampPinForm 
#追加(11/28)
from PIL import Image,ImageFilter,ImageOps
import io
from django.core.files.base import ContentFile

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
            
            obj = form.save(commit=False)
            #return redirect("home")
        
        upload_img = request.FILES["stamp_image"] #ここから画像編集に関する処理
        img = Image.open(upload_img).convert("RGB")
        
        img = ImageOps.grayscale(img)#グレースケール追加
        
        img = img.filter(ImageFilter.BLUR)#ぼかし
        
        img = img.filter(ImageFilter.SHARPEN)#シャープ
        
        img = img.filter(ImageFilter.EDGE_ENHANCE)#エッジ強調
        
        sepia = []
        r,g,b = img.split()
        
        for channel in (r,g,b):
            sepia_channel = channel.point(lambda p:p*0.9)
            
            sepia.append(sepia_channel)
            
            img = Image.merge('RGB',sepia)
            
        buffer = io.BytesIO()
        img.save(buffer,format =img.format or "JPEG")
        
        buffer.seek(0)
        
        obj.stamp_image.save(upload_img.name,ContentFile(buffer.read()),save = False)
        
        obj.save()
        
        return redirect("home") #ここまで追加(11/29)
        
        
        
        
        
        
    else:
        form = StampPinForm()
    context["form"] = form
    return render(request, template_name, context)
