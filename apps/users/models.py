from django.db import models
from apps.specialties.models import Specialty
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):

    def create_user(self, rut, dv, first_name, last_name, phone, email, password=None):
        if not rut or not dv:
            raise ValueError("Debe de ingresar el rut! ")
        
        if not email:
            raise ValueError("Debe ingresar un correo! ")

        user = self.model(
            rut = rut,
            dv = dv,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email=email),
            phone = phone,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    # TODO actualizar para técnico links de la bbdd
    def create_tech(self, rut, dv, first_name, last_name, phone, email, password=None):
        if not rut or dv:
            raise ValueError("Debe de ingresar el rut! ")
        
        if not email:
            raise ValueError("Debe ingresar un correo! ")

        user = self.model(
            rut = rut,
            dv = dv,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email=email),
            phone = phone,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, rut, dv, first_name, last_name, phone, email, password):
        
        user = self.create_user(
            rut = rut,
            dv = dv,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email=email),
            phone = phone,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    rut = models.CharField(max_length=10, primary_key=True)
    dv = models.CharField(max_length=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    # Campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    # Si queremos que email se use como login
    USERNAME_FIELD = 'email'

    # Establece los campos obligatorios
    REQUIRED_FIELDS = ['rut', 'dv', 'first_name', 'last_name', 'phone']

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    objects = MyAccountManager()

class Technician(models.Model):
    # TODO actualizar, añadir links para la demás información
    rut = models.CharField(max_length=10, primary_key=True)
    dv = models.CharField(max_length=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class TechnicianSpecialty(models.Model):
    rut_technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    id_specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("rut_technician", "id_specialty"))
