from django.db import models

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.EmailField(max_length=50)
    pass_word= models.CharField(max_length=15)
    user_type=models.IntegerField()
    


class Item(models.Model):
   
    name = models.CharField(max_length=100)
    stock_id = models.CharField(max_length=15)
    Serial_no =models.CharField(max_length=15)
    quantity=models.IntegerField()
    item_type=models.IntegerField()
    remark= models.TextField(null=True)
    

class Section(models.Model):
    name = models.CharField(max_length=100)
    section_id = models.CharField(max_length=15)
   
class Assignments(models.Model):
   
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    engineer= models.ForeignKey(Users, on_delete=models.CASCADE)
    Section= models.ForeignKey(Section, on_delete=models.CASCADE)
    remark= models.TextField(null=True)