from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.utils import verify_rut
from .models import Technician, User

class RegistrationFormUser(UserCreationForm):
    email_confirm = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("rut", "first_name", "last_name", "phone", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationFormUser, self).__init__(*args, **kwargs)
        self.fields['rut'].label = "RUT (10123456-7) "
        self.fields['phone'].label = "Teléfono (+56912345678) "
        self.fields['first_name'].label = "Nombre "
        self.fields['last_name'].label = "Apellido "
        self.fields['email'].label = "Email "
        self.fields['password1'].label = "Contraseña *"
        self.fields['password2'].label = "Confirmar Contraseña *"
        self.fields['email_confirm'].label = "Confirmar Email "

    def clean_rut(self):
        # Obtener el campo rut completo
        rut_completo = self.cleaned_data.get('rut', '')
        
        # Verificar que tenga un formato válido (RUT-DV)
        rut_completo = rut_completo.split("-") if len(rut_completo.split("-")) == 2 else None
        
        if not rut_completo:
            raise forms.ValidationError("Error, debe introducir un RUT válido en formato 10123456-1")
        
        rut = rut_completo[0]
        dv = rut_completo[1]
        dv = dv.lower() if not dv.isdigit() else dv

        # Llama a la función de verificación del RUT (suponiendo que tienes una función 'verify_rut')
        if dv != verify_rut(rut):
            raise forms.ValidationError("Por favor, verifique el RUT, el dígito verificador no es correcto.")

        # Si todo está bien, devolver el RUT limpio
        return f"{rut}-{dv}"

    # Validación personalizada para confirmar que los correos electrónicos coinciden
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')

        if email != email_confirm:
            raise forms.ValidationError("Los correos electrónicos no coinciden.")

        return cleaned_data

class RegistrationFormTech(UserCreationForm):
    email_confirm = forms.EmailField(required=True)

    class Meta:
        model = Technician
        fields = ("rut", "first_name", "last_name", "phone", "email",
                  "password1", "password2", "url_linkedin", "title", "cv", "letter")
        
        widgets = {
            'title': forms.FileInput(attrs={'accept': '.pdf'}),
            'cv': forms.FileInput(attrs={'accept': '.pdf'}),
            'letter': forms.FileInput(attrs={'accept': '.pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationFormTech, self).__init__(*args, **kwargs)
        self.fields['rut'].label = "RUT (10123456-7) "
        self.fields['phone'].label = "Teléfono (+56912345678) "
        self.fields['first_name'].label = "Nombre "
        self.fields['last_name'].label = "Apellido "
        self.fields['email'].label = "Email "
        self.fields['password1'].label = "Contraseña *"
        self.fields['password2'].label = "Confirmar Contraseña *"
        self.fields['email_confirm'].label = "Confirmar Email "
        self.fields['url_linkedin'].label = "Linkedin (URL) "
        self.fields['title'].label = "Título Académico (PDF) "
        self.fields['cv'].label = "Curriculum Vitae (PDF) "
        self.fields['letter'].label = "Carta Presentación (PDF) "

    def clean_rut(self):
        # Obtener el campo rut completo
        rut_completo = self.cleaned_data.get('rut', '')
        
        # Verificar que tenga un formato válido (RUT-DV)
        rut_completo = rut_completo.split("-") if len(rut_completo.split("-")) == 2 else None
        
        if not rut_completo:
            raise forms.ValidationError("Error, debe introducir un RUT válido en formato 10123456-1")
        
        rut = rut_completo[0]
        dv = rut_completo[1]
        dv = dv.lower() if not dv.isdigit() else dv

        # Llama a la función de verificación del RUT (suponiendo que tienes una función 'verify_rut')
        if dv != verify_rut(rut):
            raise forms.ValidationError("Por favor, verifique el RUT, el dígito verificador no es correcto.")

        # Si todo está bien, devolver el RUT limpio
        return f"{rut}-{dv}"

    # Validación personalizada para confirmar que los correos electrónicos coinciden
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')
        title = cleaned_data.get('title')
        cv = cleaned_data.get('cv')
        letter = cleaned_data.get('letter')

        if email != email_confirm:
            raise forms.ValidationError("Los correos electrónicos no coinciden.")

        if not title or not cv or not letter:
            raise forms.ValidationError("Todos los archivos (Título, CV y Carta) son obligatorios.")
        
        return cleaned_data
    