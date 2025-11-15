from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    template_name = "stampapp/home_view.html"
    context = {}
    return render(request, template_name, context)

@login_required
def google_map_view(request):
    template_name = "stampapp/google_map_view.html"
    context = {}
    return render(request, template_name, context)

@login_required
def leafret_map_view(request):
    template_name = "stampapp/leafret_map_view.html"
    context = {}
    return render(request, template_name, context)