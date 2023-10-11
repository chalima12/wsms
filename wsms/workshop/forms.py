from django import forms
from django.forms import ModelForm
from .models import Users,Item,Section,Assignments
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


class AssignmentForm(forms.ModelForm):
    # create a model choice field for the item field
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="Item")
    # create a model choice field for the engineer field
    engineer = forms.ModelChoiceField(queryset=Users.objects.filter(user_type=3,is_active=True), label="Engineer") # assume user_type 3 is engineer
    # create a model choice field for the section field
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="Section")
    # create a text area field for the remark field
    remark = forms.CharField(widget=forms.Textarea, label="Remark", required=False)

    class Meta:
        # specify the model and the fields to use
        model = Assignments
        fields = '__all__'