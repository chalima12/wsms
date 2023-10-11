from .forms import AssignmentForm
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
from .forms import UserForm

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
class itemCreateView(CreateView):
    model = Item
    fields='__all__'
    template_name = "workshop/add-tem.html"
    success_url = reverse_lazy('workshop:item')
class ComponentCreateView(CreateView):
    model = Component
    fields='__all__'
    template_name = "workshop/add_component.html"
    success_url = reverse_lazy('workshop:component')


class SectionCreateView(CreateView):
    model = Section
    fields='__all__'
    template_name = "workshop/add_section.html"
    success_url = reverse_lazy('workshop:section')

class AssignmentCreateView(CreateView):
    model = Assignments
    form_class = AssignmentForm
    template_name = "workshop/Add_assignment.html"
    success_url = reverse_lazy('workshop:assignment')

    def get_initial(self):
        # get the pk from the url kwargs
        pk = self.kwargs.get("pk")
        # get the item object or raise a 404 error
        item = get_object_or_404(Item, pk=pk)
        # set the initial value for the item field to the item object
        initial = {"item": item}
        # return the initial value
        return initial


 #view
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
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only active users
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


def delete_assignment(request,pk):
    assign=Assignments.objects.get(as_id=pk)
    if request.method=='POST':
        assign.is_valid=False
        assign.save()
        messages.success(request,  f'user {assign.as_id} has been deactivated successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/delete-assignment.html',context)




def assign_item_view(request, pk):
    form = AssignmentForm(instance=item)
    item = Item.objects.get(Serial_no=pk)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user')
    context={"item": item,"form": form}
    return render(request, "workshop/Add_assignment.html",context)

# def assign_item_view(request, pk):
#     item = get_object_or_404(Item, Serial_no=pk)
#     if request.method == "POST":
#         form = AssignmentForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect("workshop:assignment")
        
#     else:
   
#         form = AssignmentForm(instance=item)
#         context = {
#         "form": form,
#         "item": item,
#         }   
#     return render(request, "workshop/Add_assignment.html", context)
