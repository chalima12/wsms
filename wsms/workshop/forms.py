from django import forms
from django.forms import ModelForm
from .models import Users,Item,Section,Assignments,Component


class UserForm(ModelForm):
    user_name=forms.EmailField(widget=forms.EmailInput,label='Your Email')
    pass_word=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Users
        fields=['user_id','first_name','last_name','user_name','pass_word','user_type']
        widgets={
            'user_id':forms.TextInput(attrs={'class':"form-control form-control-lg",
                                             'placeholder':'Enter user id'}),
             'first_name':forms.TextInput(attrs={'class':"form-control form-control-lg",'placeholder':'Enter First Name'}),
             'last_name':forms.TextInput(attrs={'class':"form-control form-control-lg",'placeholder':'Enter Last Name' }),
             'user_name':forms.EmailInput(attrs={'class':"form-control form-control-lg",'placeholder':'Enter user Email'}),
             'pass_word':forms.PasswordInput(attrs={'class':"form-control form-control-lg"}),
             "user_type": forms.Select(attrs={"class": "form-control"}),
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
        fields = ["item", "stock_id", "Serial_no","remark"]
        widgets = {
         "item": forms.Select(attrs={"class": "form-control"}),
        "stock_id": forms.TextInput(attrs={"class": "form-control"}),
        "Serial_no": forms.TextInput(attrs={"class": "form-control"}),
        
       
        "remark": forms.Textarea(attrs={"class": "form-control"}),
        }
class SectionForm(forms.ModelForm):
    # specify the fields and widgets for the form
    class Meta:
        model = Section
        fields = ["section_id", "name", "manager"]
        widgets = {
        "section_id": forms.TextInput(attrs={"class": "form-control"}),
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "manager": forms.Select(attrs={"class": "form-control"}),
        }
        


class AssignmentForm(forms.ModelForm):
    # # create a model choice field for the item field
    # item = forms.ModelChoiceField(queryset=Item.objects.all(), label="Item")
    # # create a model choice field for the engineer field
    # engineer = forms.ModelChoiceField(queryset=Users.objects.filter(user_type=3,is_active=True), label="Engineer") # assume user_type 3 is engineer
    # # create a model choice field for the section field
    # Section = forms.ModelChoiceField(queryset=Section.objects.filter(is_valid=True), label="Section")
    # # create a text area field for the remark field
    # remark = forms.CharField(widget=forms.Textarea, label="Remark", required=False)

    class Meta:
        # specify the model and the fields to use
        model = Assignments
        fields = ["as_id", "item", "engineer",'Section',"remark"]
        widgets = {
        "as_id": forms.TextInput(attrs={"class": "form-control"}),
        "item": forms.HiddenInput(attrs={"class": "form-control"}),
        "engineer":forms.Select(attrs={"class":"form-control"}),
        "Section": forms.Select(attrs={"class": "form-control"}),
        "remark": forms.Textarea(attrs={"class": "form-control"}),
        }
       
class AcceptForm(forms.Form):
    model=Assignments
    # create a hidden field for the assignment id
    assignment_id = forms.CharField(widget=forms.HiddenInput())
    # create a submit button for the accept action
    accept = forms.BooleanField( label='Accept', required = True, 
                                widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}), 
                                 )