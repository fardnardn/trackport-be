from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    ItemListCreateView, ItemDetailView,
    ShipmentListCreateView, ShipmentDetailView
)

urlpatterns = [
    # User API URLs
    path('api/users/', UserListCreateView.as_view(), name='user_list_create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Item API URLs
    path('api/items/', ItemListCreateView.as_view(), name='item_list_create'),
    path('api/items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),

    # Shipment API URLs
    path('api/shipments/', ShipmentListCreateView.as_view(), name='shipment_list_create'),
    path('api/shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment_detail'),
]
