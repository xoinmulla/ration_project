# beneficiary_management/models.py
from django.db import models
from django.conf import settings # To link to the User model

class RationCard(models.Model):
    CARD_TYPE_CHOICES = [
        ('APL', 'Above Poverty Line'),
        ('BPL', 'Below Poverty Line'),
        ('AAY', 'Antyodaya Anna Yojana'),
    ]
    card_number = models.CharField(max_length=50, unique=True)
    holder_name = models.CharField(max_length=100) # Or link to a UserProfile
    card_type = models.CharField(max_length=3, choices=CARD_TYPE_CHOICES)
    address = models.TextField()
    # primary_beneficiary_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ration_card_holder')
    issued_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.card_number} - {self.holder_name}"

class Beneficiary(models.Model):
    ration_card = models.ForeignKey(RationCard, related_name='members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=gender_choices)
    # user_account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='beneficiary_profile')
    # Add other relevant fields like Aadhaar number, relation to card holder, etc.

    def __str__(self):
        return f"{self.name} (Card: {self.ration_card.card_number})"