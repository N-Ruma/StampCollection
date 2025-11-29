from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    template_name = "stampapp/home_view.html"
    context = {}
    return render(request, template_name, context)