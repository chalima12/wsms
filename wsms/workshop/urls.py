
from django.urls import path
from .import views
app_name = 'workshop'

urlpatterns = [
    # view
    path('', views.index),
    
    #  path("register-item", views.register_item, name="register-item"),
     path("user",views.UserListView.as_view()  ,name="user"),
     path("item",views.ItemListView.as_view() , name="item"),
     path("component",views.ComponentListView.as_view() , name="component"),
     path('section', views.SectionListView.as_view(), name='section'),
     path('assignment', views.AssignmentListView.as_view(), name='assignment'),
     path("tictac",views.tictac , name="tictac"),
    #  path('delete', views.delete, name='delete'),
   #create
     path('create-item', views.itemCreateView.as_view(),name='create-item'),
     path('create-component', views.ComponentCreateView.as_view(),name='create-component'),
     path("register", views.UserCreateView.as_view(), name="register"),
     path('create-section', views.SectionCreateView.as_view(),name='create-section'),
     path('create-assignment', views.assign_item_view,name='create-assignment'),
# delete
path("delete-user/<str:pk>",views.delete_user ,name="delete-user"),
path('item_delete/<int:pk>',views.ItemDeleteView.as_view(), name='user_delete'),

]
