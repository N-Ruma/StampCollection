from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def register_view(request):
    template_name = "accounts/register.html"
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # ログイン
            login(request, form.save())
            return redirect("home")
    else:
        form = UserCreationForm()
    context["form"] = form
    return render(request, template_name, context)

def login_view(request):
    template_name = "accounts/login.html"
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # ログイン
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    context["form"] = form
    return render(request, template_name, context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")
    
