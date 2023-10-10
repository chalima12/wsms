from django import forms
from django.forms import ModelForm
from .models import Users,Item

class UserForm(ModelForm):
    user_name=forms.EmailField(widget=forms.EmailInput,label='Your Email')
    pass_word=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Users
        fields=['user_id','first_name','last_name','user_name','pass_word','user_type']
        widget={
            'user_id':forms.TextInput(attrs={'class':"form-control form-control-lg"}),
             'first_name':forms.TextInput(attrs={'class':"form-control form-control-lg"}),
             'last_name':forms.TextInput(attrs={'class':"form-control form-control-lg"}),
             'user_name':forms.EmailInput(attrs={'class':"form-control form-control-lg"}),
             'pass_word':forms.PasswordInput(attrs={'class':"form-control form-control-lg"}),
             'user_id':forms.Select(attrs={'class':"form-control form-control-lg"}),
        }


class ItemForm(ModelForm):
    class Meta:
        model=Item
        fields='__all__'


class AssignForm(ModelForm):
    class Meta:
        # model=Assignments
        fields='__all__'