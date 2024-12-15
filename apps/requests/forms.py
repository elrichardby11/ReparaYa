from django import forms

from apps.services.models import Service
from .models import Quotation, QuotationService
from django.forms import modelformset_factory

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['estimated_cost', 'estimated_duration', 'location', 'comment']

class QuotationServiceForm(forms.ModelForm):
    class Meta:
        model = QuotationService
        fields = ['service', 'price']

    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="Seleccione un servicio")


QuotationServiceFormSet = modelformset_factory(
    QuotationService,
    fields=("service", "price"),
    extra=0,
    can_delete=True
)
