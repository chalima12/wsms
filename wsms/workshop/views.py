from .forms import AssignForm

from django.http import HttpResponseRedirect
from django.shortcuts import  redirect, render
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
    fields='__all__'
    template_name = "workshop/item.html"
    success_url = reverse_lazy('workshop:assignment')





 


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

   
class ComponentListView(ListView):
    model = Component
    context_object_name='components'
    template_name="workshop/component.html"
    # paginate_by = 4 # if pagination is desired


class SectionListView(ListView):
    model = Section
    context_object_name='sections'
    template_name="workshop/section.html"
    # paginate_by = 4 # if pagination is desired

class AssignmentListView(ListView):
    model = Assignments
    context_object_name='forms'
    template_name="workshop/Assignment.html"
    # paginate_by = 4 # if pagination is desired
 

# delete
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy("item")

class UserDeleteView(DeleteView):
    model = Users
    context_object_name='user'
    template_name="workshop/user.html"

    success_url = reverse_lazy("user")





def assign_item_view(request, Serial_no):
    item = Item.objects.get(id=Serial_no)
    if request.method == 'POST':
        form = AssignForm(request.POST, initial={'item': item.Serial_no})
        if form.is_valid():
            form.save()
        return redirect('asignment')
    else:
        form = AssignForm(initial={'item': item.Serial_no})
        return render(request, 'Add_assignment.html', {'form': form, 'item': item})




def delete_user(request,pk):
    user=Users.objects.get(user_id=pk)
    if request.method=='POST':
        user.is_active=False
        user.save()
        messages.success(request,  f'user {user.first_name} {user.last_name} has been deactivated successfully.')
        return redirect('/user')
    context={'user':user}
    return render(request,'workshop/delete-user.html',context)


# @require_POST
# def delete_object(request):
# # get the object id from the form data
# object_id = request.POST.get("object_id")
# # get the object or raise a 404 error
# object = get_object_or_404(Object, id=object_id)
# # delete the object
# object.delete()
# # redirect to another page
# return redirect("home")
