from rest_framework import generics
from .models import User, Item, Shipment
from .serializers import UserSerializer, ItemSerializer, ShipmentSerializer

#  Logic for our backend API



# USERS CRUD



#  Authentication
#  - User Registration
#  - User Login
#  - User Logout
#  - User forgot password
#  - User change password
#  - User activate accout

#  items
#  - receive an items at the docking point
#  - view all items by logged in user


# shipments
# - view all shipments by logged in user
#  - assign to a driver for dispatch
#  - update shipment status


#  User Tracking
#  - view all shipments by logged in customer
#  - view all shipments by logged in user
#  - update shipment status by driver
#  - Mark shipment as delivered/the others

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
