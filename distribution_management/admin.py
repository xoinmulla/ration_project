from django.contrib import admin
from .models import RationItem, Stock, DistributionRecord, DistributionItemDetail

class DistributionItemDetailInline(admin.TabularInline):
    model = DistributionItemDetail
    extra = 1

class DistributionRecordAdmin(admin.ModelAdmin):
    list_display = ('ration_card', 'date_of_distribution', 'total_amount')
    search_fields = ('ration_card__card_number',)
    list_filter = ('date_of_distribution',)
    inlines = [DistributionItemDetailInline]
    # readonly_fields = ('total_amount',) # If calculated automatically

admin.site.register(RationItem)
admin.site.register(Stock)
admin.site.register(DistributionRecord, DistributionRecordAdmin)
admin.site.register(DistributionItemDetail) # Usually managed via inline