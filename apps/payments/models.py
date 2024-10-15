from django.db import models
from apps.requests.models import Request

class PaymentMethod(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"

class Payment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    amount = models.IntegerField()
    id_payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of {self.amount} for request {self.request.id}'
