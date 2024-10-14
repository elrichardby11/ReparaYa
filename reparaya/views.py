from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def register_user(request):
    return render(request, "register_user.html")

def register_tech(request):
    return render(request, "register_tech.html")