# beneficiary_management/urls.py
from django.urls import path
from . import views
from .views import ration_card_list_view, ration_card_create_view, ration_card_detail_view, ration_card_update_view, ration_card_delete_view
from .views import beneficiary_add_to_card_view, beneficiary_update_view, beneficiary_delete_view



app_name = 'beneficiary_management' # Optional: for namespacing URLs

urlpatterns = [
    path('', ration_card_list_view, name='ration_card_list'),
    path('ration_card/add/', ration_card_create_view, name='ration_card_create'),
    path('ration_card/<str:card_number>/', ration_card_detail_view, name='ration_card_detail'),
    path('ration_card/<str:card_number>/edit/', ration_card_update_view, name='ration_card_update'),
    path('ration_card/<str:card_number>/delete/', ration_card_delete_view, name='ration_card_delete'),

    # You might have separate views for beneficiaries or manage them inline with ration cards
    path('ration_card/<str:card_number>/add_beneficiary/', beneficiary_add_to_card_view, name='beneficiary_add_to_card'),
    path('beneficiary/<int:pk>/edit/', beneficiary_update_view, name='beneficiary_update'),
    path('beneficiary/<int:pk>/delete/', beneficiary_delete_view, name='beneficiary_delete'),


]