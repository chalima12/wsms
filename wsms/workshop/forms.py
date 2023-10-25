from django import forms
from django.forms import ModelForm
from .models import *


class UserForm(ModelForm):
    # user_name=forms.EmailField(widget=forms.EmailInput,label='Your Email')
    # pass_word=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','user_name','pass_word','user_type']
        widgets={
             'first_name':forms.TextInput(attrs={'class':"form-control form-control"
                                                 ,'placeholder':'Enter First Name'}),
             'last_name':forms.TextInput(attrs={'class':"form-control form-control",'placeholder':'Enter Last Name' }),
             'user_name':forms.EmailInput(attrs={'class':"form-control form-control",'placeholder':'Enter user Email'}),
             'pass_word':forms.PasswordInput(attrs={'class':"form-control form-control",'placeholder':'Enter user password'}),
             "user_type": forms.Select(attrs={"class": "form-control",'placeholder':'Enter user Email'}),
        }

class ItemForm(forms.ModelForm):
    # specify the fields and widgets for the form
    class Meta:
        model = Item
        fields = ["ws_id", "stock_id", "Serial_no", "delivered_by", "received_by", "remark"]
        widgets = {
        "ws_id": forms.TextInput(attrs={"class": "form-control"}),
        "stock_id": forms.TextInput(attrs={"class": "form-control"}),
        "Serial_no": forms.TextInput(attrs={"class": "form-control"}),
        "delivered_by": forms.TextInput(attrs={"class": "form-control"}),
        "received_by": forms.TextInput(attrs={"class": "form-control"}),
        "remark": forms.Textarea(attrs={"class": "form-control"}),
        }
        
            

class ComponentForm(forms.ModelForm):
    # specify the fields and widgets for the form
    class Meta:
        model = Component
        fields = ["item", "stock_id", "Serial_no"]
        widgets = {
         "item": forms.HiddenInput(attrs={"class": "form-control"}),
        "stock_id": forms.TextInput(attrs={"class": "form-control"}),
        "Serial_no": forms.TextInput(attrs={"class": "form-control"}),
        
       
        # "remark": forms.Textarea(attrs={"class": "form-control"}),
        }
class SectionForm(forms.ModelForm):
    manager = forms.ModelChoiceField(queryset=User.objects.filter(user_type='Manager'
                ,is_active=True), label="Engineer",
                widget=forms.Select(attrs={"class":"form-control"})) 
    class Meta:
        model = Section
        fields = [ "name", "manager"]
        widgets = {
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "manager": forms.Select(attrs={"class": "form-control"}),
        }
        


class AssignmentForm(forms.ModelForm):
    
    engineer = forms.ModelChoiceField(queryset=User.objects.filter(user_type='Engineer'
                ,is_active=True), label="Engineer",
                widget=forms.Select(attrs={"class":"form-control"})) # assume user_type 3 is engineer
    Section = forms.ModelChoiceField(queryset=Section.objects.filter(is_valid=True), 
            label="Section",widget=forms.Select(attrs={"class":"form-control"}))
    class Meta:
        model=Assignments
        fields = ["item", "engineer",'Section',"remark"]
        widgets = {
        "item": forms.HiddenInput(attrs={"class": "form-control"}),
        "engineer":forms.Select(attrs={"class":"form-control"}),
        "Section": forms.Select(attrs={"class": "form-control"}),
        "remark": forms.Textarea(attrs={"class": "form-control"}),
        }



