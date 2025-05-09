# distribution_management/forms.py
from django import forms
from .models import RationItem, Stock, DistributionRecord, DistributionItemDetail
from beneficiary_management.models import RationCard

class RationItemForm(forms.ModelForm):
    class Meta:
        model = RationItem
        fields = ['name', 'unit', 'price_per_unit']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item', 'quantity'] # 'last_updated' is auto

class DistributionRecordForm(forms.ModelForm):
    ration_card_number = forms.CharField(label="Ration Card Number", max_length=50)

    class Meta:
        model = DistributionRecord
        fields = ['ration_card_number'] # 'date_of_distribution' is auto, 'total_amount' calculated

    def clean_ration_card_number(self):
        card_number = self.cleaned_data.get('ration_card_number')
        try:
            RationCard.objects.get(card_number=card_number, is_active=True)
        except RationCard.DoesNotExist:
            raise forms.ValidationError("Active ration card with this number does not exist.")
        return card_number

class DistributionItemDetailForm(forms.ModelForm):
    class Meta:
        model = DistributionItemDetail
        fields = ['item', 'quantity_distributed'] # 'price_at_distribution' set in view

DistributionItemDetailFormSet = forms.inlineformset_factory(
    DistributionRecord,
    DistributionItemDetail,
    form=DistributionItemDetailForm,
    fields=['item', 'quantity_distributed'],
    extra=1,
    can_delete=True
)