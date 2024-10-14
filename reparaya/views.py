from django.shortcuts import redirect, render

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type', '')

        if user_type == 'user':
            return redirect('register_user')
        elif user_type == 'tech':
            return redirect('register_tech')

    return render(request, 'register.html')

def register_user(request):
    return render(request, "register_user.html")

def register_tech(request):
    return render(request, "register_tech.html")