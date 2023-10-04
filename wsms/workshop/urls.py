
from django.urls import path
from .import views
app_name="workshop"

urlpatterns = [
    path('', views.index),
     path("register", views.UserCreateView.as_view(), name="register"),
    #  path("register-item", views.register_item, name="register-item"),
     path("user",views.user ,name="user"),
     path("item",views.item , name="item"),
     path("tictac",views.tictac , name="tictac"),
     path('delete', views.delete, name='delete'),
     path('assign', views.assign_item, name='assign'),
     path('create-item', views.itemCreateView.as_view(),name='create-item'),
     


]
