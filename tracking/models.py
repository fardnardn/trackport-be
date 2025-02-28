from django.db import models
# from django.db.models import Abs

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('driver', 'Driver'),
        ('receiver', 'Receiver'),
    ]
   
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    docking_point = models.ForeignKey('DockingPoint', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.email


class DockingPoint(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('others', 'Others'),
    ]

    owner_id = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shipments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    receiver = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    tracking_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tracking_code


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.BooleanField(default=False)  # False means unread, True means read

    def __str__(self):
        return f'Notification for {self.user.email}'