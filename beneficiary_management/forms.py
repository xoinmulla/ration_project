# beneficiary_management/forms.py
from django import forms
from .models import RationCard, Beneficiary

class RationCardForm(forms.ModelForm):
    class Meta:
        model = RationCard
        fields = ['card_number', 'holder_name', 'card_type', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        # 'ration_card' will usually be set programmatically or via URL,
        # or selected if adding beneficiary to an existing card through a specific interface.
        fields = ['name', 'age', 'gender']

class BeneficiaryInlineFormSetHelper(forms.ModelForm): # Example if using inline formsets
    class Meta:
        model = Beneficiary
        fields = ['name', 'age', 'gender']

BeneficiaryFormSet = forms.inlineformset_factory(
    RationCard,
    Beneficiary,
    form=BeneficiaryInlineFormSetHelper,
    fields=['name', 'age', 'gender'],
    extra=1, # Number of empty forms
    can_delete=True
)