# distribution_management/views.py
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Add if needed
from django.contrib import messages
from django.db import transaction
from .models import RationItem, Stock, DistributionRecord, DistributionItemDetail
from beneficiary_management.models import RationCard # To link distribution to a card
from .forms import RationItemForm, StockForm, DistributionRecordForm, DistributionItemDetailFormSet

# --- Ration Item Views ---
@login_required
def ration_item_list_view(request):
    items = RationItem.objects.all()
    return render(request, 'distribution_management/ration_item_list.html', {'items': items})

@login_required
def ration_item_create_view(request):
    if request.method == 'POST':
        form = RationItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            # Optionally create initial stock for this item
            Stock.objects.create(item=item, quantity=0)
            messages.success(request, f'Ration Item "{item.name}" created successfully and initial stock set to 0.')
            return redirect('distribution_management:ration_item_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RationItemForm()
    return render(request, 'distribution_management/ration_item_form.html', {'form': form, 'title': 'Create Ration Item'})

@login_required
def ration_item_update_view(request, pk):
    item = get_object_or_404(RationItem, pk=pk)
    if request.method == 'POST':
        form = RationItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ration Item "{item.name}" updated successfully.')
            return redirect('distribution_management:ration_item_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RationItemForm(instance=item)
    return render(request, 'distribution_management/ration_item_form.html', {'form': form, 'item': item, 'title': 'Update Ration Item'})

@login_required
def ration_item_delete_view(request, pk):
    item = get_object_or_404(RationItem, pk=pk)
    if request.method == 'POST':
        item_name_display = item.name
        # Consider implications: what if stock or distribution records exist for this item?
        # You might want to prevent deletion or handle it gracefully.
        item.delete()
        messages.success(request, f'Ration Item "{item_name_display}" deleted successfully.')
        return redirect('distribution_management:ration_item_list')
    return render(request, 'distribution_management/ration_item_confirm_delete.html', {'item': item})


# --- Stock Views ---
@login_required
def stock_list_view(request):
    stocks = Stock.objects.select_related('item').all()
    return render(request, 'distribution_management/stock_list.html', {'stocks': stocks})

@login_required
def stock_update_view(request, pk): # Typically, stock is updated by adding new supplies
    stock_item = get_object_or_404(Stock, pk=pk)
    # This view is simplified; a real stock update might involve a form for adding quantity
    if request.method == 'POST':
        # Example: form = StockUpdateQuantityForm(request.POST)
        # if form.is_valid():
        #    added_quantity = form.cleaned_data['quantity_to_add']
        #    stock_item.quantity += added_quantity
        #    stock_item.save()
        #    messages.success(request, f"Stock for {stock_item.item.name} updated.")
        #    return redirect('distribution_management:stock_list')
        # For now, let's use the StockForm directly for editing the total quantity
        form = StockForm(request.POST, instance=stock_item)
        if form.is_valid():
            form.save() # last_updated will be set automatically
            messages.success(request, f"Stock for {stock_item.item.name} updated.")
            return redirect('distribution_management:stock_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StockForm(instance=stock_item)
    return render(request, 'distribution_management/stock_form.html', {'form': form, 'stock_item': stock_item, 'title': 'Update Stock'})


# --- Distribution Record Views ---
@login_required
def distribution_record_list_view(request):
    records = DistributionRecord.objects.select_related('ration_card').all().order_by('-date_of_distribution')
    return render(request, 'distribution_management/distribution_record_list.html', {'records': records})

@login_required
def distribution_record_create_view(request):
    if request.method == 'POST':
        form = DistributionRecordForm(request.POST)
        formset = DistributionItemDetailFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic(): # Ensures all operations succeed or none do
                    ration_card_number = form.cleaned_data['ration_card_number']
                    ration_card = RationCard.objects.get(card_number=ration_card_number)

                    distribution_record = DistributionRecord(ration_card=ration_card)
                    # 'operator' field if you have it: distribution_record.operator = request.user
                    distribution_record.save() # Save record first to get an ID for formset

                    total_amount_calculated = 0
                    items_distributed = formset.save(commit=False)

                    for item_detail in items_distributed:
                        if item_detail.item_id is None or item_detail.quantity_distributed is None or item_detail.quantity_distributed <= 0:
                            # Skip empty or invalid forms in the formset if not marked for deletion
                            if not (hasattr(item_detail, 'cleaned_data') and item_detail.cleaned_data.get('DELETE')):
                                continue

                        # Check stock
                        stock_item = Stock.objects.get(item=item_detail.item)
                        if stock_item.quantity < item_detail.quantity_distributed:
                            messages.error(request, f"Not enough stock for {item_detail.item.name}. Available: {stock_item.quantity}")
                            # Rollback transaction by raising an error or returning early
                            raise forms.ValidationError(f"Not enough stock for {item_detail.item.name}.")

                        stock_item.quantity -= item_detail.quantity_distributed
                        stock_item.save()

                        item_detail.distribution_record = distribution_record
                        item_detail.price_at_distribution = item_detail.item.price_per_unit # Price at time of distribution
                        item_detail.save()
                        total_amount_calculated += (item_detail.price_at_distribution * item_detail.quantity_distributed)

                    if not formset.forms_valid_and_not_empty(): # Check if any actual items were added
                         messages.error(request, "No items were added to the distribution record.")
                         raise forms.ValidationError("No items added.")


                    distribution_record.total_amount = total_amount_calculated
                    distribution_record.save()

                    messages.success(request, f'Distribution record for card {ration_card.card_number} created successfully.')
                    return redirect('distribution_management:distribution_record_detail', pk=distribution_record.pk)

            except RationCard.DoesNotExist:
                messages.error(request, "Invalid Ration Card number.")
            except forms.ValidationError as e: # Catch validation errors raised manually (like stock error)
                 pass # Messages already set
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors in the form(s) below.")
    else:
        form = DistributionRecordForm()
        formset = DistributionItemDetailFormSet(prefix='items', queryset=DistributionItemDetail.objects.none())

    return render(request, 'distribution_management/distribution_record_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Distribution Record'
    })


@login_required
def distribution_record_detail_view(request, pk):
    record = get_object_or_404(DistributionRecord.objects.select_related('ration_card')
                               .prefetch_related('items_distributed__item'), pk=pk)
    return render(request, 'distribution_management/distribution_record_detail.html', {'record': record})

@login_required
def distribution_record_delete_view(request, pk):
    record = get_object_or_404(DistributionRecord, pk=pk)
    if request.method == 'POST':
        # Important: Deleting a distribution record should ideally revert stock changes.
        # This requires careful implementation to avoid inconsistencies.
        # For simplicity, this basic delete does not revert stock.
        # In a real system, you might "cancel" a record rather than hard delete,
        # or implement a stock adjustment logic here.
        with transaction.atomic():
            for item_detail in record.items_distributed.all():
                stock_item = Stock.objects.get(item=item_detail.item)
                stock_item.quantity += item_detail.quantity_distributed # Revert stock
                stock_item.save()
            record_id_display = record.id
            record.delete()
            messages.success(request, f'Distribution Record ID {record_id_display} deleted and stock reverted.')
        return redirect('distribution_management:distribution_record_list')
    return render(request, 'distribution_management/distribution_record_confirm_delete.html', {'record': record})

# Helper for distribution_record_create_view formset validation
def forms_valid_and_not_empty(self):
    is_valid = True
    has_actual_data = False
    for form in self.forms:
        if hasattr(form, 'cleaned_data') and form.cleaned_data and not form.cleaned_data.get('DELETE', False):
            has_actual_data = True
        if form.errors:
            is_valid = False
    return is_valid and has_actual_data

DistributionItemDetailFormSet.forms_valid_and_not_empty = forms_valid_and_not_empty