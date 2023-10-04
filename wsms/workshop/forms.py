from django.forms import ModelForm
from .models import *

class UserForm(ModelForm):
    class Meta:
        model=Users
        fields='__all__'


class ItemForm(ModelForm):
    class Meta:
        model=Item
        fields='__all__'


class AssignForm(ModelForm):
    class Meta:
        # model=Assignments
        fields='__all__'