from django.db import models
from django.conf import settings

class OzonOrder(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    order_number = models.CharField(max_length=50)
    posting_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    in_process_at = models.DateTimeField(null=True, blank=True)
    cancel_reason_id = models.IntegerField(null=True, blank=True)
    product_names = models.TextField()
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    warehouse_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_commission = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    schema = models.CharField(max_length=3)  # FBO или FBS
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.order_number}"

    class Meta:
        ordering = ['-created_at']
