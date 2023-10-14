from .forms import *
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect
from django.shortcuts import  get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (View,
                                  DateDetailView,
                                  CreateView,
                                  UpdateView,
                                  DetailView
                                  ,DeleteView,
                                  ListView)
from .models import *
from django.contrib import messages
from .forms import UserForm,ItemForm,ComponentForm

def tictac(request_iter):
    return  render(request_iter,'workshop/data.html')
def index(request_iter):
    return  render(request_iter,'workshop/base1.html')


class UserCreateView(CreateView):
    model = Users
    # fields='__all__'
    form_class=UserForm
    template_name = "workshop/register.html"
    def form_valid(self, form):
        # get the user object from the form
        user = form.save(commit=False)
        # get the plain text password from the form data
        password = form.cleaned_data["pass_word"]
        # hash the password and save it to the user object
        user.set_password(password)
        # save the user to the database
        user.save()
        # return the default form_valid behavior
        return super().form_valid(form)
    success_url = reverse_lazy('workshop:user')
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "workshop/add-tem.html"
    success_url = reverse_lazy('workshop:item')
class ComponentCreateView(CreateView):
    model = Component
    form_class=ComponentForm
    template_name = "workshop/add_component.html"
    success_url = reverse_lazy('workshop:component')


class SectionCreateView(CreateView):
    model = Section
    form_class=SectionForm
    template_name = "workshop/add_section.html"
    success_url = reverse_lazy('workshop:section')


class AssignmentCreateView(CreateView):
    # specify the form class
    form_class = AssignmentForm
    # specify the template name
    template_name = "workshop/Add_assignment.html"
    # specify the success url
    success_url = reverse_lazy('workshop:assignment')
    def get_initial(self):
        # get the initial data for the form
        initial = super().get_initial()
        # get the item object from the url parameter
        item = Item.objects.get(Serial_no=self.kwargs['serial_no'])
        # set the initial value for the item field
        initial['item'] = item
        return initial
    
    def form_valid(self, form):
        # change the status of the item to 2 (accepted)
        form.instance.item.status = 2
        # save the item object
        form.instance.item.save()
        # call the superclass method to save the assignment object
        return super().form_valid(form)

class UserListView(ListView):
    model = Users

    context_object_name='users'
    template_name="workshop/user.html"
    def get_queryset(self):
# return only active users
        return Users.objects.filter(is_active=True)
class ItemListView(ListView):
    model = Item
    st=Item.status
    context_object_name='items'
    template_name="workshop/item.html"
    # paginate_by = 10 # if pagination is desired
    def get_queryset(self):
    # return only active users
        return Item.objects.filter(is_valid=True)
   
class ComponentListView(ListView):
    model = Component
    context_object_name='components'
    template_name="workshop/component.html"
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only active users
        return Component.objects.filter(is_valid=True)

class SectionListView(ListView):
    model = Section
    context_object_name='sections'
    template_name="workshop/section.html"
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only active users
        return Section.objects.filter(is_valid=True)
class AssignmentListView(ListView):
    model = Assignments
    context_object_name='forms'
    template_name="workshop/Assignment.html"
    def get_queryset(self):
        return Assignments.objects.filter(is_valid=True)

 

# delete
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy("item")

class UserDeleteView(DeleteView):
    model = Users
    context_object_name='user'
    template_name="workshop/user.html"

    success_url = reverse_lazy("user")


def delete_user(request,pk):
    user=Users.objects.get(user_id=pk)
    if request.method=='POST':
        user.is_active=False
        user.save()
        messages.success(request,  f'user {user.first_name} {user.last_name} has been deactivated successfully.')
        return redirect('/user')
    context={'user':user}
    return render(request,'workshop/delete-user.html',context)
# delete Item
def delete_item(request,pk):
    item=Item.objects.get(Serial_no=pk)
    if request.method=='POST':
        item.is_valid=False
        item.save()
        messages.success(request,  f'user {item.Serial_no} has been deactivated successfully.')
        return redirect('/item')
    context={'item':item}
    return render(request,'workshop/delete-item.html',context)

def delete_component(request,pk):
    component=Component.objects.get(Serial_no=pk)
    if request.method=='POST':
        component.is_valid=False
        component.save()
        messages.success(request,  f'user {component.Serial_no} has been deactivated successfully.')
        return redirect('/component')
    context={'component':component}
    return render(request,'workshop/delete-component.html',context)


def delete_section(request,pk):
    section=Section.objects.get(section_id=pk)
    if request.method=='POST':
        section.is_valid=False
        section.save()
        messages.success(request,  f'user {section.section_id} has been deactivated successfully.')
        return redirect('/section')
    context={'section':section}
    return render(request,'workshop/delete-section.html',context)

#accept Assignment
class AcceptView(View):
    # specify the form class
    form_class = AcceptForm
    # specify the template name
    template_name = 'workshop/accept_form.html'

    def get(self, request, *args, **kwargs):
        # get the assignment object from the url parameter
        assignment = Assignments.objects.get(as_id=self.kwargs['as_id'])
        # create a form with the assignment id as initial value
        form = self.form_class(initial={'assignment_id': assignment.as_id})
        # render the template with the form
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # get the form data from the request
        form = self.form_class(request.POST)
        # validate the form
        if form.is_valid():
        # get the assignment id from the form data
         assignment_id = form.cleaned_data['assignment_id']
        # get the assignment object from the database
        assignment = Assignments.objects.get(as_id=assignment_id)
        # get the item object from the assignment object
        item = assignment.item
        # change the is_accepted field of the item to True
        item.is_accepted = True
        # save the item object
        item.save()
        # redirect to the assignments list page
        return redirect('/assignment')


def delete_assignment(request,pk):
    assign=Assignments.objects.get(as_id=pk)
    
    if request.method=='POST':
        assign.is_valid=False
        assign.save()
        messages.success(request,  f'user {assign.as_id} has been deactivated successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/delete-assignment.html',context)

# def add_item_view(request):
#     if request.method == "POST":
#         item =Item.Serial_no
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             if item  in form:
#                 Item.Repeat_Count+=1
#                 form.save()
            
#             form.save()
#             return redirect("workshop:item")
#     else:
#         form = ItemForm()
#     context = {
#     "form": form,
#     }
    
#     return render(request, "workshop/add-tem.html", context)






"""
Completed Task
1.Add User and display List of then as table
2.Add Item  and display List of then as table
3.Add Section and display List of then as table
4.Add Component and display List of then as table
5.Assign Item to Engineer and display List of then as table

If accidentally error data added the system allow them to delete
1.Delete user : Change is_active to false(deactivate)
2.Delete Item : Change is_valid to false(invalidate)
3.Delete Section : Change is_valid to false(invalidate)
4.Delete Assignment : Change is_valid to false(invalidate)

Remaing Task
1.Accept an Assignment 
2.Complete Assignment 
3.genarate Report
4.Usre Authantication
5.Middleware (give access and role to Users)
"""