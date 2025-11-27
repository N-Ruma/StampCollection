from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def mainView(request):
    
    options = {
        
    }
    return render(request, 'picchange.html', options)

def apploadView(request):
    
    options = {
        
    }
    return render(request, 'picappload.html', options)

def stampView(request):
    
    options = {
        
    }
    return render(request, 'stamp.html', options)

def stampappView(request):
    
    options = {
        
    }
    return render(request, 'appload.html', options)


def upload_image(request):
    print("🌟 upload_image が呼ばれた！ method =", request.method) # ←追加

    if request.method == 'POST':
        print("📥 POST を受け取りました") # ←追加
        print("FILES =", request.FILES) # ←追加

        file = request.FILES.get('image')

        if not file:
            print("❌ file が空！") # ←追加
            return JsonResponse({'error': '画像が送られていません'}, status=400)

        from django.core.files.storage import default_storage
        save_path = default_storage.save('uploaded/' + file.name, file)

        print("✅ 保存成功:", save_path) # ←追加

        return JsonResponse({
            'message': 'アップロード完了！',
            'file_name': file.name,
            'saved_to': save_path,
        })

    print("❌ POST 以外の method だった") # ←追加
    return JsonResponse({'error': 'POST で送ってください'}, status=400)
