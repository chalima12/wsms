from .forms import *
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import  get_object_or_404, redirect, render
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
    model = User
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
    def get_initial(self):
        # get the initial data for the form
        initial = super().get_initial()
        # get the item object from the url parameter
        ass = Assignments.objects.get(id=self.kwargs['id'])
        item=ass.item
        # set the initial value for the item field
        initial['item'] = item
        return initial
    


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
        item = Item.objects.get(id=self.kwargs['id'])
        # set the initial value for the item field
        initial['item'] = item
        return initial
    def form_valid(self, form):
        # save the form and get the assignment object
        assignment = form.save()
        # get the item object from the assignment object
        item = assignment.item
        # change the status of the item to on progress
        item.status = 'on progress'
        # save the item object
        item.save()
        # return the default form valid response
        return super().form_valid(form)

    class UserListView(ListView):
        model = User

        context_object_name='users'
        template_name="workshop/user.html"
        def get_queryset(self):
    # return only active users
            return User.objects.filter(is_active=True)

class UserListView(ListView):
    model = User

    context_object_name='users'
    template_name="workshop/user.html"
    def get_queryset(self):
# return only active users
        return User.objects.filter(is_active=True)
    

class ItemListView(ListView):
    model = Item
    st=Item.status
    context_object_name='items'
    template_name="workshop/item.html"
    # paginate_by = 10 # if pagination is desired
    def get_queryset(self):
    # return only valid item
        return Item.objects.filter(is_valid=True)
   
class ComponentListView(ListView):
    model = Component
    context_object_name='components'
    template_name="workshop/component.html"
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only valid item
        return Component.objects.filter(is_valid=True)

class SectionListView(ListView):
    model = Section
    context_object_name='sections'
    template_name="workshop/section.html"
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only valid section
        return Section.objects.filter(is_valid=True)
class AssignmentListView(ListView):
    model = Assignments
    
    context_object_name='assignments'
    template_name="workshop/Assignment.html"
    def get_queryset(self):
        return Assignments.objects.filter(is_valid=True)
    

class ReporttListView(ListView):
    model = Assignments
    
    context_object_name='assignments'
    template_name="workshop/report.html"
    def get_queryset(self):
        return Assignments.objects.filter(is_valid=True)
def delete_user(request,pk):
    user=User.objects.get(id=pk)
    if request.method=='POST':
        user.is_active=False
        user.save()
        messages.success(request,  f'user {user.first_name} {user.last_name} has been deactivated successfully.')
        return redirect('/user')
    context={'user':user}
    return render(request,'workshop/delete-item.html',context)


# delete Item
def delete_item(request,pk):
    item=Item.objects.get(id=pk)
    if request.method=='POST':
        item.is_valid=False
        item.save()
        messages.success(request,  f'user {item.Serial_no} has been deactivated successfully.')
        return redirect('/item')
    context={'item':item}
    return render(request,'workshop/delete-item.html',context)

def delete_component(request,pk):
    component=Component.objects.get(id=pk)
    if request.method=='POST':
        component.is_valid=False
        component.save()
        messages.success(request,  f'Componente {component.Serial_no} has been deactivated successfully.')
        return redirect('/component')
    context={'component':component}
    return render(request,'workshop/delete-item.html',context)


def delete_section(request,pk):
    section=Section.objects.get(id=pk)
    if request.method=='POST':
        section.is_valid=False
        section.save()
        messages.success(request,  f'Section {section.name} has been deactivated successfully.')
        return redirect('/section')
    context={'section':section}
    return render(request,'workshop/delete-item.html',context)

def delete_assignment(request,pk):
    assign=Assignments.objects.get(id=pk)
    
    if request.method=='POST':
        assign.is_valid=False
        assign.save()
        messages.success(request,  f'user {assign.id} has been deactivated successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/delete-assignment.html',context)


def accept_assignment(request,id):
    assign=Assignments.objects.get(id=id)
    item=assign.item
    if request.method=='POST':
        item.is_accepted=True

        item.save()
        messages.success(request,  f'Assignment {assign.id} has been accepted successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/accept_form.html',context)


def complete_assignment(request,pk):
    assign=Assignments.objects.get(id=pk)
    item=assign.item
    if request.method=='POST':
        item.status='completed'
        assign.completed_date=timezone.now()
        assign.save()
        item.save()
        messages.success(request,  f'Assignment {assign.id} has been completed successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/accept_form.html',context)



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
1.Accept an Assignment 
2.Complete Assignment 
3.genarate Report

Remaing Task


4.Usre Authantication
5.Middleware (give access and role to Users)
6.Dashboard
"""