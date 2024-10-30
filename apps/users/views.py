from django.shortcuts import redirect, render
from django.contrib import auth, messages

from apps.specialties.models import Specialty
from apps.users.forms import RegistrationFormUser, RegistrationFormTech
from apps.users.models import Technician, TechnicianSpecialty, User
from apps.users.utils import verify_rut
from django.contrib.auth import login, authenticate


import json

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
        form = RegistrationFormUser(request.POST)
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
        form = RegistrationFormUser()
    
    return render(request, 'register_user.html', {'form': form})

def register_tech(request):
    if request.method == 'POST':
        form = RegistrationFormTech(request.POST)
        if form.is_valid():
            # Procesar RUT
            rut_completo = str(form.cleaned_data['rut']).split("-")
            if len(rut_completo) != 2:
                messages.error(request, "Error, debe introducir un RUT válido! (10123456-1)")
                return render(request, 'register_tech.html', {'form': form})

            rut = rut_completo[0]
            dv = rut_completo[1].lower() if not rut_completo[1].isdigit() else rut_completo[1]

            # Verificar el RUT
            if dv != verify_rut(rut):
                messages.error(request, "Por favor, verifique el RUT!")
                return render(request, 'register_tech.html', {'form': form})

            # Crea el usuario
            user = form.save(commit=False)
            user.dv = dv
            user.rut = rut
            user.is_active = True
            request.session['tech_rut'] = rut
            form.save(commit=True)
            return redirect('device_selection')
        
        else:
            # Mostrar errores específicos para cada campo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = RegistrationFormTech()
    
    return render(request, 'register_tech.html', {'form': form})

def device_selection(request):
    if request.method == 'POST':
        selected_devices = json.loads(request.POST.get('selected_devices', '[]'))
        rut = request.session.get('tech_rut', '')

        if not selected_devices:
            return render(request, 'register_tech2.html', {'error': 'Por favor, seleccione al menos un dispositivo.'})

        if not rut:
            return render(request, 'register_tech.html', {'error': 'Por favor, vuelva a registrarse.'})

        for name in selected_devices:
            technician = Technician.objects.filter(rut=rut).first()
            specialty = Specialty.objects.filter(name=name).first()
            tech_specialty = TechnicianSpecialty.objects.create(
                rut_technician=technician,
                id_specialty=specialty)

        del request.session['tech_rut']
        messages.success(request, "Registro exitoso. Puedes iniciar sesión.")
        return redirect('login')

    return render(request, 'register_tech2.html')

"""
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
"""

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentar autenticar en el modelo User
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # Solo pasa el request y el usuario
            return redirect('home')  # Redirigir al dashboard o página inicial

        # Intentar autenticar en el modelo Technician si no se encontró en User
        technician = authenticate(request, email=email, password=password, backend='apps.users.backends.CustomBackend')
        if technician is not None:
            login(request, technician)  # Solo pasa el request y el usuario
            return redirect('home')  # Redirigir al dashboard o página inicial

        messages.error(request, 'Credenciales inválidas. Inténtalo nuevamente.')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')