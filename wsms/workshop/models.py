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
    pass_word= models.CharField(max_length=15)
    user_type = models.CharField(choices=user_type,default="Engineer")
    is_active=models.BooleanField(auto_created=True,default=True)
    is_staff = models.BooleanField(default=True,null=True,auto_created=True,blank=True)
    is_superuser = models.BooleanField(default=False,auto_created=True,null=True,blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff
   
    def __str__(self) -> str:
        return f"{self.first_name.upper()} {self.last_name.upper()}"
    # def get_absolute_url (self):
    #     return reverse("workshop:index")

class Item(models.Model):
    """
    This is the item model  has five fields name,stock_id,serial_no,
    status(pending,accepted,completed,not maintable),remark
    """
    ws_id = models.CharField(max_length=15)
    received_date=models.DateField(auto_now=1)
    stock_id = models.CharField(max_length=15)
    Serial_no =models.CharField(max_length=15)
    delivered_by = models.CharField(max_length=100)
    received_by= models.CharField(max_length=100)
    status = models.CharField(choices=(
          ('pending', "pending"),
          ('on_prograss', "On_progress"),
           ('completed', "Completed"),
            ('Not maintainable', "Not maintanable"),
          ),default='pending' ,
          auto_created=True
          )
    remark= models.TextField(blank=True)
    comment= models.TextField(blank=True)
    is_valid=models.BooleanField(auto_created=True,default=True)
    is_accepted=models.BooleanField(auto_created=True,default=False)
    is_maintainable=models.BooleanField(auto_created=True,default=True)

    def __str__(self) -> str:
        return self.Serial_no
    def get_absolute_url (self):
        return reverse("workshop:item")
    
class Component(models.Model):
    recived_date=models.DateField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='components')
    stock_id = models.CharField(max_length=15)
    Serial_no =models.CharField(max_length=15)
    is_valid=models.BooleanField(auto_created=True,default=True)

    
 

    
    def __str__(self) -> str:
        return self.Serial_no
    def get_absolute_url (self):
        return reverse("workshop:component")

class Section(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    is_valid=models.BooleanField(default=True)

   
    def __str__(self) -> str:
        return self.name
class Assignments(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    engineer= models.ForeignKey(User, on_delete=models.CASCADE)
    Section= models.ForeignKey(Section, on_delete=models.CASCADE)
    remark= models.TextField(blank=True)
    Assigned_date=models.DateField(auto_now=True)
    completed_date=models.DateField(default="2023-11-02",auto_created=True)
    is_valid=models.BooleanField(auto_created=True,default=True)

    def __str__(self) -> str:
        return str(self.item)
