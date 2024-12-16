from django.shortcuts import get_object_or_404, redirect, render
from apps.services.models import Service
from apps.users.decorators import technician_required, user_required
from apps.specialties.models import Specialty
from django.contrib import messages
from apps.users.models import Technician, TechnicianSpecialty
from .models import Quotation, QuotationService, Request
from datetime import datetime
from .forms import QuotationForm, QuotationServiceFormSet

# USER

@user_required
def requests(request, id=None):
    if request.method == "POST":
        return redirect("user_requests")

    requests_history = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    context = {"repair_history": requests_history}

    if id:
        user_request = get_object_or_404(Request, id=id, rut_user=request.user.rut)
        context["request"] = user_request

    template_name = "user_request_detail.html" if id else "user_requests.html"
    
    return render(request, template_name, context)

@user_required
def add_request(request):
    requests_history = Request.objects.filter(rut_user=request.user.rut).order_by('-created_at')[:5]
    specialties = Specialty.objects.all()

    if request.method == "POST":
        date = datetime.today().strftime('%Y-%m-%d')
        image = request.FILES.get("image")
        device_type_id = request.POST.get("device_type", "")
        title = request.POST.get("title", "")
        comment = request.POST.get("problem_description", "")

        try:
            user = request.user
            device_type = Specialty.objects.get(id=device_type_id)

            Request.objects.create(
                rut_user=user,
                request_date=date,
                id_specialty=device_type,
                request_image=image,
                title=title,
                comment=comment,
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

@user_required
def technicians(request, id=None):
    if request.method == "POST":
        return redirect("technicians")

    #Buscar técnicos interesados
    user_requests = Request.objects.filter(rut_user=request.user.rut, id_status=1)
    interested_technicians = Quotation.objects.filter(request_id__in=user_requests).order_by('-created_at')[:5]

    context = {"techs": interested_technicians,}

    if id:
        quotation = Quotation.objects.filter(id=id).first()
        services = QuotationService.objects.filter(quotation=quotation)
        context.update({
            "services": services,
        })

        context["quotation"] = quotation

    template_name = "user_technician_detail.html" if id else "user_technicians.html"

    return render(request, template_name, context=context)

# TECH

@technician_required
def tech_requests(request, id=None):
    if request.method == "POST":
        return redirect("tech_requests")
    
    # Consulta para saber todas las solicitudes que puede reparar el técnico de acuerdo a lo que sabe reparar
    technician_rut = request.user.rut
    available_requests = Request.objects.filter(
        id_specialty__in=TechnicianSpecialty.objects.filter(rut_technician=technician_rut).values('id_specialty'),
    ).exclude(id_status_id__in=[2, 3]).order_by("-created_at")[:5]
    
    context = {"available_requests": available_requests}

    if id:
        solicitud = get_object_or_404(Request, id=id, id_status=1,
                                      id_specialty__in=TechnicianSpecialty.objects.filter(rut_technician=technician_rut)
                                      .values('id_specialty'))
        # Buscar si tiene cotización
        quotation = Quotation.objects.filter(request=solicitud, technician__rut=request.user.rut).first()
        services = QuotationService.objects.filter(quotation=quotation)
        context.update({
            "quotation": quotation,
            "services": services,
        })
        context["request"] = solicitud

    template_name = "tech_request_detail.html" if id else "tech_requests.html"
    
    return render(request, template_name, context)

@technician_required
def create_quotation(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    services = Service.objects.all()

    if request.method == "POST":
        form = QuotationForm(request.POST)
        formset = QuotationServiceFormSet(request.POST, queryset=QuotationService.objects.none())

        if form.is_valid() and formset.is_valid():
            quotation = form.save(commit=False)
            quotation.request = request_obj
            quotation.technician = get_object_or_404(Technician, rut=request.user.rut)
            quotation.save()

            for form in formset:
                if form.cleaned_data:
                    service = form.save(commit=False)
                    service.quotation = quotation
                    service.save()

            messages.success(request, "¡Cotización creada con éxito!")
            return redirect("tech_request_detail", id=request_id)
        else:
            messages.error(request, "Hubo un error al guardar los datos.")

    else:
        form = QuotationForm()
        formset = QuotationServiceFormSet(queryset=QuotationService.objects.none())

    return render(request, 'quotations/create_quotation.html', {
        'form': form,
        'formset': formset,
        'services': services,
    })