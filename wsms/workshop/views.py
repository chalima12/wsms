from django.http import HttpResponseRedirect
from django.shortcuts import  redirect, render
from django.urls import reverse
from django.views.generic import (View,
                                  DateDetailView,
                                  CreateView,
                                  UpdateView,
                                  DetailView
                                  ,DeleteView)
from .import models
from .forms import *

def tictac(request_iter):
    return  render(request_iter,'workshop/game.html')
def index(request_iter):
    return  render(request_iter,'workshop/index.html')
# def register_request(request):
#     form=UserForm()
#     if request.method=="POST":
#         form=UserForm(request.POST)
#         if form.is_valid:
#             form.save()
    
#     context = {'form':form}
#     return HttpResponseRedirect(reverse('register'))
class UserCreateView(CreateView):
    model = Users
    fields='__all__'
    template_name = "workshop/register.html"


class itemCreateView(CreateView):
    model = Item
    fields='__all__'
    template_name = "workshop/add-tem.html"


def assign_item(request):
    form=AssignForm()
    if request.method=="POST":
        form=AssignForm(request.POST)
        if form.is_valid:
            form.save()
    
    context = {'form':form}
    return reverse('workshop:assign')
    



def user(request):
    form = Users.objects.all()
    context = {'form':form}
    return  render(request,'workshop/user.html',context)

def item(request):
    form = Item.objects.all()
    context = {'form':form}
    return  render(request,'workshop/item.html',context)
def delete(id):
   Users.objects.filter(id=id).delete()
   return HttpResponseRedirect(reverse('user'))