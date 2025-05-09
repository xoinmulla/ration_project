# authentication/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
        ('beneficiary', 'Beneficiary'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='beneficiary')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Add other profile-specific fields

    def __str__(self):
        return self.user.username

# Optional: Signal to create/update UserProfile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()