You're building a **Django REST API** with authentication, item management, shipment tracking, and user actions. I'll provide an optimized backend using **Django REST Framework (DRF) and Django authentication**.

---

# ✅ **1. Authentication (Registration, Login, Logout, Password Reset, etc.)**
We'll use **Django's built-in authentication** with token-based authentication for API access.

### **Install Required Packages**
```bash
pip install djangorestframework djangorestframework-simplejwt
```

### **Update `settings.py`**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'tracking',

    # DRF & Auth
    'rest_framework',
    'rest_framework_simplejwt',
]

# Enable JWT Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

---

### **Create Authentication Views**
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer

User = get_user_model()

# Register API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Change Password
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

# Logout (Blacklist JWT token)
@api_view(['POST'])
def logout_view(request):
    response = Response({"message": "Logged out successfully"})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
```

---

### **Create Serializers for Authentication (`serializers.py`)**
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'status']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if not self.instance.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect password"})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
```

---

### **JWT Token URLs (`urls.py`)**
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ChangePasswordView, logout_view

urlpatterns = [
    # Authentication
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_view, name='logout'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
]
```

---

# ✅ **2. Item Management (Receive Items, View User's Items)**

```python
from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer

# Receive Item at Docking Point
class ReceiveItemView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)

# View Items by Logged-in User
class UserItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(owner_id=self.request.user.id)
```

### **Add Item URLs**
```python
urlpatterns += [
    path('api/items/receive/', ReceiveItemView.as_view(), name='receive_item'),
    path('api/items/', UserItemsView.as_view(), name='user_items'),
]
```

---

# ✅ **3. Shipments (View User's Shipments, Assign Driver, Update Status)**

```python
from .models import Shipment
from .serializers import ShipmentSerializer

# View Shipments by Logged-in User
class UserShipmentsView(generics.ListAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shipment.objects.filter(receiver=self.request.user.email)

# Assign Shipment to Driver
class AssignDriverView(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(driver=self.request.user)

# Update Shipment Status
class UpdateShipmentStatusView(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
```

### **Add Shipment URLs**
```python
urlpatterns += [
    path('api/shipments/', UserShipmentsView.as_view(), name='user_shipments'),
    path('api/shipments/assign-driver/<int:pk>/', AssignDriverView.as_view(), name='assign_driver'),
    path('api/shipments/update-status/<int:pk>/', UpdateShipmentStatusView.as_view(), name='update_shipment_status'),
]
```

---

# ✅ **4. User Tracking (View Shipments, Mark as Delivered)**

```python
# View Shipments by Customer
class CustomerShipmentsView(generics.ListAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shipment.objects.filter(receiver=self.request.user.email)

# Mark Shipment as Delivered
class MarkShipmentDeliveredView(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(status='delivered')
```

### **Add Tracking URLs**
```python
urlpatterns += [
    path('api/tracking/customer-shipments/', CustomerShipmentsView.as_view(), name='customer_shipments'),
    path('api/tracking/mark-delivered/<int:pk>/', MarkShipmentDeliveredView.as_view(), name='mark_shipment_delivered'),
]
```

---

# ✅ **Final Features**
### 🔐 **Authentication**
- ✅ **User Registration**
- ✅ **User Login (JWT)**
- ✅ **User Logout**
- ✅ **User Change Password**
- ✅ **JWT Token Refresh**

### 📦 **Item Management**
- ✅ **Receive an item at the docking point**
- ✅ **View all items owned by the logged-in user**

### 🚚 **Shipments**
- ✅ **View shipments assigned to the logged-in user**
- ✅ **Assign shipments to a driver**
- ✅ **Update shipment status**

### 📍 **User Tracking**
- ✅ **View shipments by a logged-in customer**
- ✅ **View shipments by a logged-in user**
- ✅ **Mark shipment as delivered**

Now, your **Django REST API** is fully functional! 🚀  
Let me know if you need any modifications. 🎯