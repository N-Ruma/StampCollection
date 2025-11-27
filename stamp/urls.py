from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'stamp'

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.mainView,name = 'stamp'),
    path('app',views.apploadView,name = 'app'),
    path('star',views.stampView,name = 'star'),
    path('appload',views.stampappView,name = 'appload'),
    path('upload-image',views.upload_image,name = 'upload_image'),
]