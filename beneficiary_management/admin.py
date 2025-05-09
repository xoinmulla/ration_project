from django.contrib import admin
from .models import RationCard, Beneficiary

class BeneficiaryInline(admin.TabularInline): # Or admin.StackedInline
    model = Beneficiary
    extra = 1 # Number of empty forms to display

class RationCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'holder_name', 'card_type', 'is_active', 'issued_date')
    search_fields = ('card_number', 'holder_name')
    list_filter = ('card_type', 'is_active')
    inlines = [BeneficiaryInline]

admin.site.register(RationCard, RationCardAdmin)
admin.site.register(Beneficiary)