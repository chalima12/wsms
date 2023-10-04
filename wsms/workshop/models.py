from django.db import models
from django.urls import reverse, reverse_lazy

class Users(models.Model):
    user_id=models.CharField(max_length=50,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.EmailField(max_length=50)
    pass_word= models.CharField(max_length=15)
    user_type = models.IntegerField(choices=(
          (1, "manager"),
          (2, "registeror"),
          (3, "Engineer"),
          
          ),default=3
          )
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    def get_absolute_url (self):
        return reverse("workshop:user")

class Item(models.Model):
    """
    This is the item model  has five fields name,stock_id,serial_no,
    status(pending,accepted,completed,not maintable),remark
    """
    ws_id = models.CharField(max_length=15)
    received_date=models.DateField(auto_now=1)
    stock_id = models.CharField(max_length=15)
    Serial_no =models.CharField(max_length=15,primary_key=True)
    delivered_by = models.CharField(max_length=100)
    received_by= models.CharField(max_length=100)
    status = models.IntegerField(choices=(
          (1, "pending"),
          (2, "accepted"),
           (3, "Completed"),
            (4, "Not maintanable"),
          ),default=1
          )
    remark= models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.stock_id},{self.Serial_no}"
    def get_absolute_url (self):
        return reverse("workshop:item")
    
class Component(models.Model):
    recived_date=models.DateField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    stock_id = models.CharField(max_length=15)
    Serial_no =models.CharField(max_length=15,primary_key=True)
    remark= models.TextField(blank=True)
    
    def __str__(self) -> str:
        return f"{self.stock_id} {self.Serial_no}"

class Section(models.Model):
    section_id = models.CharField(max_length=15,primary_key=True)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(Users, on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return f"{self.name}"
class Assignments(models.Model):
    as_id=models.CharField(max_length=100,primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    engineer= models.ForeignKey(Users, on_delete=models.CASCADE)
    Section= models.ForeignKey(Section, on_delete=models.CASCADE)
    remark= models.TextField(blank=True)
    Assigned_date=models.DateField(auto_now=True)
    completed_date=models.DateField(default="2023-11-02")
    def __str__(self) -> str:
        return f"{self.as_id}"
