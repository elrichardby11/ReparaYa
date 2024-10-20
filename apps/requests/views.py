from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from apps.specialties.models import Specialty
from apps.users.models import User
from django.contrib import messages

from .models import Request
from datetime import datetime

@login_required
def requests(request, id=None):
    if request.method == "POST":
        return redirect("requests")

    requests_history = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    context = {"repair_history": requests_history}

    if id:
        solicitud = get_object_or_404(Request, id=id)
        context["request"] = solicitud

    template_name = "request_detail.html" if id else "requests.html"
    
    return render(request, template_name, context)

@login_required
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
            return redirect("requests")

        except Exception as e:
            messages.error(request, f"Se ha producido un error: {e}. Por favor, verifique los datos.")
            return redirect("login")

    context = {
        "repair_history": requests_history,
        "specialties": specialties,
    }

    return render(request, "request_new.html", context)
