# distribution_management/urls.py
from django.urls import path
from . import views

app_name = 'distribution_management'

urlpatterns = [
    path('items/', views.ration_item_list_view, name='ration_item_list'),
    path('item/add/', views.ration_item_create_view, name='ration_item_create'),
    path('item/<int:pk>/edit/', views.ration_item_update_view, name='ration_item_update'),
    path('item/<int:pk>/delete/', views.ration_item_delete_view, name='ration_item_delete'),

    path('stock/', views.stock_list_view, name='stock_list'),
    path('stock/<int:pk>/update/', views.stock_update_view, name='stock_update'),
    # Stock creation might be tied to ration item creation or a separate process

    path('records/', views.distribution_record_list_view, name='distribution_record_list'),
    path('record/new/', views.distribution_record_create_view, name='distribution_record_create'),
    path('record/<int:pk>/', views.distribution_record_detail_view, name='distribution_record_detail'),
    path('record/<int:pk>/delete/', views.distribution_record_delete_view, name='distribution_record_delete'),
]