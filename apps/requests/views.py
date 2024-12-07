from django.shortcuts import get_object_or_404, redirect, render
from apps.users.decorators import technician_required, user_required
from apps.specialties.models import Specialty
from django.contrib import messages
from apps.users.models import TechnicianSpecialty
from .models import Request
from datetime import datetime

# USER

@user_required
def requests(request, id=None):
    if request.method == "POST":
        return redirect("user_requests")

    requests_history = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    context = {"repair_history": requests_history}

    if id:
        solicitud = get_object_or_404(Request, id=id, rut_user=request.user.rut)
        context["request"] = solicitud

    template_name = "user_request_detail.html" if id else "user_requests.html"
    
    return render(request, template_name, context)

@user_required
def add_request(request):
    requests_history = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    specialties = Specialty.objects.all()

    if request.method == "POST":
        date = datetime.today().strftime('%Y-%m-%d')
        device_type_id = request.POST.get("device_type", "")
        title = request.POST.get("title")
        comment_user = request.POST.get("problem_description")

        try:
            user = request.user
            device_type = Specialty.objects.get(id=device_type_id)

            Request.objects.create(
                rut_user=user,
                request_date=date,
                id_specialty=device_type,
                title=title,
                customer_comment=comment_user,
            )

            messages.success(request, "¡Se ha creado una solicitud de reparación!")
            return redirect("user_requests")

        except Exception as e:
            messages.error(request, f"Se ha producido un error: {e}. Por favor, verifique los datos.")
            return redirect("login")

    context = {
        "repair_history": requests_history,
        "specialties": specialties,
    }

    return render(request, "user_request_new.html", context)

# TECH

@technician_required
def tech_requests(request, id=None):
    if request.method == "POST":
        return redirect("tech_requests")
    
    # Consulta para saber todas las solicitudes que puede
    # reparar el técnico de acuerdo a lo que sabe reparar
    technician_rut = request.user.rut
    available_requests = Request.objects.filter(
    id_specialty__in=TechnicianSpecialty.objects.filter(rut_technician=technician_rut).values('id_specialty'),
    ).exclude(id_status_id__in=[2, 3]).order_by("-created_at")[:5]
    
    context = {"available_requests": available_requests}

    if id:
        solicitud = get_object_or_404(Request, id=id, id_status=1,
                                      id_specialty__in=TechnicianSpecialty.objects.filter(rut_technician=technician_rut)
                                      .values('id_specialty'))
        context["request"] = solicitud

    template_name = "tech_request_detail.html" if id else "tech_requests.html"
    
    return render(request, template_name, context)