# distribution_management/models.py
from django.db import models
from beneficiary_management.models import RationCard

class RationItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20) # e.g., KG, Litre
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Stock(models.Model):
    item = models.ForeignKey(RationItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2) # Current stock
    last_updated = models.DateTimeField(auto_now=True)
    # You might want to link stock to a specific distribution center if you have multiple

    def __str__(self):
        return f"{self.item.name}: {self.quantity} {self.item.unit}"

class DistributionRecord(models.Model):
    ration_card = models.ForeignKey(RationCard, on_delete=models.CASCADE)
    date_of_distribution = models.DateTimeField(auto_now_add=True)
    # operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='distributions_done')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Distribution to {self.ration_card.card_number} on {self.date_of_distribution.strftime('%Y-%m-%d')}"

class DistributionItemDetail(models.Model):
    distribution_record = models.ForeignKey(DistributionRecord, related_name='items_distributed', on_delete=models.CASCADE)
    item = models.ForeignKey(RationItem, on_delete=models.CASCADE)
    quantity_distributed = models.DecimalField(max_digits=10, decimal_places=2)
    price_at_distribution = models.DecimalField(max_digits=10, decimal_places=2) # Price per unit at the time of distribution

    def __str__(self):
        return f"{self.quantity_distributed} {self.item.unit} of {self.item.name} for Record ID {self.distribution_record.id}"