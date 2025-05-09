# beneficiary_management/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Add if needed
from django.contrib import messages
from .models import RationCard, Beneficiary
from .forms import RationCardForm, BeneficiaryForm, BeneficiaryFormSet

@login_required # Example, adjust permissions as needed
def ration_card_list_view(request):
    ration_cards = RationCard.objects.all().order_by('-issued_date')
    query = request.GET.get('q')
    if query:
        ration_cards = ration_cards.filter(card_number__icontains=query) | \
                       ration_cards.filter(holder_name__icontains=query)
    return render(request, 'beneficiary_management/ration_card_list.html', {'ration_cards': ration_cards})

@login_required
def ration_card_create_view(request):
    if request.method == 'POST':
        form = RationCardForm(request.POST)
        if form.is_valid():
            ration_card = form.save()
            messages.success(request, f'Ration Card {ration_card.card_number} created successfully.')
            return redirect('beneficiary_management:ration_card_detail', card_number=ration_card.card_number)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RationCardForm()
    return render(request, 'beneficiary_management/ration_card_form.html', {'form': form, 'title': 'Create Ration Card'})

@login_required
def ration_card_detail_view(request, card_number):
    ration_card = get_object_or_404(RationCard, card_number=card_number)
    beneficiaries = ration_card.members.all() # Using related_name 'members'
    return render(request, 'beneficiary_management/ration_card_detail.html', {'ration_card': ration_card, 'beneficiaries': beneficiaries})

@login_required
def ration_card_update_view(request, card_number):
    ration_card = get_object_or_404(RationCard, card_number=card_number)
    if request.method == 'POST':
        form = RationCardForm(request.POST, instance=ration_card)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ration Card {ration_card.card_number} updated successfully.')
            return redirect('beneficiary_management:ration_card_detail', card_number=ration_card.card_number)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RationCardForm(instance=ration_card)
    return render(request, 'beneficiary_management/ration_card_form.html', {'form': form, 'ration_card': ration_card, 'title': 'Update Ration Card'})

@login_required
def ration_card_delete_view(request, card_number):
    ration_card = get_object_or_404(RationCard, card_number=card_number)
    if request.method == 'POST':
        card_num_display = ration_card.card_number
        ration_card.delete()
        messages.success(request, f'Ration Card {card_num_display} deleted successfully.')
        return redirect('beneficiary_management:ration_card_list')
    return render(request, 'beneficiary_management/ration_card_confirm_delete.html', {'ration_card': ration_card})


# --- Beneficiary Views (Example: could be integrated with Ration Card update using formsets) ---
@login_required
def beneficiary_add_to_card_view(request, card_number):
    ration_card = get_object_or_404(RationCard, card_number=card_number)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            beneficiary = form.save(commit=False)
            beneficiary.ration_card = ration_card
            beneficiary.save()
            messages.success(request, f'Beneficiary {beneficiary.name} added to card {ration_card.card_number}.')
            return redirect('beneficiary_management:ration_card_detail', card_number=ration_card.card_number)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BeneficiaryForm()
    return render(request, 'beneficiary_management/beneficiary_form.html', {'form': form, 'ration_card': ration_card, 'title': 'Add Beneficiary'})

@login_required
def beneficiary_update_view(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, instance=beneficiary)
        if form.is_valid():
            form.save()
            messages.success(request, f'Beneficiary {beneficiary.name} updated successfully.')
            return redirect('beneficiary_management:ration_card_detail', card_number=beneficiary.ration_card.card_number)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BeneficiaryForm(instance=beneficiary)
    return render(request, 'beneficiary_management/beneficiary_form.html', {'form': form, 'beneficiary': beneficiary, 'ration_card': beneficiary.ration_card, 'title': 'Update Beneficiary'})

@login_required
def beneficiary_delete_view(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    ration_card_number = beneficiary.ration_card.card_number
    if request.method == 'POST':
        beneficiary_name_display = beneficiary.name
        beneficiary.delete()
        messages.success(request, f'Beneficiary {beneficiary_name_display} deleted successfully.')
        return redirect('beneficiary_management:ration_card_detail', card_number=ration_card_number)
    return render(request, 'beneficiary_management/beneficiary_confirm_delete.html', {'beneficiary': beneficiary})


