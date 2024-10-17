from django.shortcuts import redirect, render
from django.contrib import auth, messages

from apps.users.forms import RegistrationForm
from apps.users.utils import verify_rut

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(request, email=email, password=password)
        
        if user is None:
            messages.error(request, "Clave incorrecta .Vuelva a Intentar (Recuerde que el campo password es sensible a mayúsculas y minúsculas).")
            return redirect('login')
        
        auth.login(request, user)
        return redirect('home')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type', '')

        if user_type == 'user':
            return redirect('register_user')
        elif user_type == 'tech':
            return redirect('register_tech')

    return render(request, 'register.html')

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Procesar RUT
            rut_completo = str(form.cleaned_data['rut']).split("-")
            if len(rut_completo) != 2:
                messages.error(request, "Error, debe introducir un RUT válido! (10123456-1)")
                return render(request, 'register_user.html', {'form': form})

            rut = rut_completo[0]
            dv = rut_completo[1].lower() if not rut_completo[1].isdigit() else rut_completo[1]

            # Verificar el RUT
            if dv != verify_rut(rut):
                messages.error(request, "Por favor, verifique el RUT!")
                return render(request, 'register_user.html', {'form': form})

            # Crea el usuario
            user = form.save(commit=False)
            user.dv = dv
            user.rut = rut
            user.is_active = True
            form.save(commit=True)
            messages.success(request, "Registro exitoso. Puedes iniciar sesión.")
            return redirect('login')
        
        else:
            # Mostrar errores específicos para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = RegistrationForm()
    
    return render(request, 'register_user.html', {'form': form})

def register_tech(request):
    messages.success(request, "Solicitud enviada correctamente")    
    return render(request, "register_tech.html")

def logout(request):
    auth.logout(request)
    return redirect('home')