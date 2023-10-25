
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
app_name = 'workshop'

urlpatterns = [
    # view
    path('', views.index,name='index'),
    path('home', views.index,name='index'),
    
    #  path("register-item", views.register_item, name="register-item"),
     path("user",views.UserListView.as_view()  ,name="user"),
     path("item",views.ItemListView.as_view() , name="item"),
     path("component",views.ComponentListView.as_view() , name="component"),
     path('section', views.SectionListView.as_view(), name='section'),
     path('assignment', views.AssignmentListView.as_view(), name='assignment'),
     path('report', views.ReporttListView.as_view(), name='report'),
    #  path('delete', views.delete, name='delete'),
   #create
     path('create-item', views.ItemCreateView.as_view(),name='create-item'),
     path('create-component/<str:id>', views.ComponentCreateView.as_view(),name='create-component'),
     path("register", views.UserCreateView.as_view(), name="register"),
     path('create-section', views.SectionCreateView.as_view(),name='create-section'),
     path('create-assignment/<str:id>', views.AssignmentCreateView.as_view(),name='create-assignment'),
    #  path('save_assignment', views.save_assignment_view,name='save_assignment'),
     

# delete
path("delete-user/<str:pk>",views.delete_user ,name="delete-user"),
path('item_delete/<str:pk>',views.delete_item, name='item_delete'),
path("accept-assignment/<str:id>",views.accept_assignment ,name="accept"),
path('conponent-delete/<str:pk>',views.delete_component, name='conponent-delete'),
path("delete-section/<str:pk>",views.delete_section ,name="section-delete"),
path('complete-assignment/<int:pk>/', views.complete_assignment, name='complete'),

path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
path('login/', views.custom_login, name='custom_login'),



]
