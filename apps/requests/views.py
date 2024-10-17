from django.shortcuts import get_object_or_404, redirect, render

from apps.specialties.models import Specialty
from apps.users.models import User
from django.contrib import messages

from .models import Request

from datetime import datetime

def requests(request, id=None):

    if request.method == "POST":
        return redirect("requests")

    if id:
        solicitud = get_object_or_404(Request, id=id)
        requests = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
        context = {"request": solicitud,
                   "repair_history": requests,}
    else:
        requests = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
        context = {"repair_history": requests,}

    return render(request, "requests.html" if not id else "request_detail.html", context=context)

def add_request(request):
    requests = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    specialties = Specialty.objects.all()
    
    if request.method == "POST":
        date = datetime.today().strftime('%Y-%m-%d')
        device_type_id = request.POST["device_type"] if request.POST["device_type"] else ""
        title = request.POST["title"]
        comment_user = request.POST["problem_description"]

        try:
            user = User.objects.get(rut=request.user.rut)
            device_type = Specialty.objects.get(id=device_type_id)

            req = Request.objects.create(
                rut_user=user,
                request_date = date,
                id_specialty = device_type,
                title = title,
                customer_comment = comment_user,
            )

            messages.success(request, "Se ha creado una solicitud de reparación! ")
            return redirect("requests")

        except Exception as e:
            messages.error(request, e, "Se ha producido un error, por favor, verifique los datos! ")
            return redirect("login")

    context = {"repair_history": requests,
               "specialties": specialties,}

    return render(request, "request_new.html", context=context)