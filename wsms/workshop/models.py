import django
import uuid 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse, reverse_lazy
# from .forms import *
user_type=[('Manager', "manager"),
          ('Registeror', "registeror"),
          ('Engineer', "Engineer"),]
class User(AbstractBaseUser,PermissionsMixin):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.EmailField(max_length=50,unique=1)
    pass_word= models.CharField(max_length=50)
    user_type = models.CharField(choices=user_type,default="Engineer",max_length=20)
    is_active=models.BooleanField(auto_created=True,default=True)
    is_staff = models.BooleanField(default=True,null=True,auto_created=True,blank=True)
    is_superuser = models.BooleanField(default=False,auto_created=True,null=True,blank=True)
    view_dashboard = models.BooleanField(default=True,null=True,auto_created=True,blank=True)
    # for role and permision
    is_admin = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_user = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_item = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_component = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_assignment = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_section = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    view_report = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    add_user = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    add_item = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    add_component = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    add_assignment = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    add_section = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    delete_user = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    delete_item = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    delete_component = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    delete_section = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    delete_assignment = models.BooleanField(default=False,null=True,auto_created=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    


    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff
   
    def __str__(self) -> str:
        return f"{self.first_name.upper()} {self.last_name.upper()}"
class Stock(models.Model):
    number = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f" {self.id}. {self.number} ({self.description})"

class Section(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE,related_name='manage_sections')
    is_valid=models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self) -> str:
        return self.name
class Item(models.Model):
    """
    This is the item model  has five fields name,stock_id,serial_no,
    status(pending,accepted,completed,not maintable),remark
    """
    
    received_date = models.DateField(auto_created=True, default=django.utils.timezone.now)
    Section= models.ForeignKey(Section, on_delete=models.CASCADE,related_name='sections')
    engineer= models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='engineers')
    stock_id = models.ForeignKey(Stock,on_delete=models.CASCADE, related_name='stocks')
    Serial_no =models.CharField(max_length=15)
    region = models.CharField(max_length=100,null=True,blank=True)
    branch = models.CharField(max_length=100,null=True,blank=True)
    delivered_by= models.CharField(max_length=100)
    status = models.CharField(choices=(
          ('pending', "pending"),
          ('Damage', "Damage"),
           ('completed', "Completed"),
          ),default='pending' ,
          auto_created=True,
          max_length=20
          )
    remark= models.TextField(blank=False,null=False)
    comment= models.TextField(blank=False,null=False)
    is_valid=models.BooleanField(auto_created=True,default=True)
    is_accepted=models.BooleanField(auto_created=True,default=False)
    is_damage=models.BooleanField(auto_created=True,default=False)
    is_maintainable_onfield=models.BooleanField(auto_created=True,default=False)
    assigned=models.BooleanField(auto_created=True,default=False)
    completed_date=models.DateField(blank=True,null=True)

    def __str__(self) -> str:
        return self.Serial_no
    def get_absolute_url (self):
        return reverse("workshop:item")
    
class Component(models.Model):
    recived_date=models.DateField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='components')
    stock_id = models.ForeignKey(Stock,on_delete=models.CASCADE, related_name='component_stock')
    quantity =models.IntegerField(default=1)
    is_valid=models.BooleanField(auto_created=True,default=True)

    
 

    
    def __str__(self) -> str:
        return self.Serial_no
    def get_absolute_url (self):
        return reverse("workshop:component")


class AssignmentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-Assigned_date')
class Assignments(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='items')
    engineer= models.ForeignKey(User, on_delete=models.CASCADE)
    remark= models.TextField(blank=False,null=False)
    Assigned_date=models.DateField(auto_now=True)
    completed_date=models.DateField(blank=True,null=True)
    is_valid=models.BooleanField(auto_created=True,default=True)

    def __str__(self) -> str:
        return str(self.item)

class Notification(models.Model):
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('read', 'Read')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(null=True)
    link = models.CharField(max_length=255, null=True)

    def mark_as_read(self):
        if self.status == 'pending':
            self.status = 'read'
            self.save()
