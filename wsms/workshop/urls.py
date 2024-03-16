
from django.urls import path,include
from django.contrib.auth import views as auth_views
from .import views
app_name = 'workshop'
from .views import autocomplete_view

# urls.py
from django.urls import path
from .views import ItemCreateView, StockSearchView
from .views import send_password_reset_email, password_reset, reset_expired






urlpatterns = [
    # view
     path('item_status_chart/', views.item_status_chart, name='item_status_chart'),
    path('analysis/', views.analysis_view, name='analysis'),
     path('stock-search/', StockSearchView.as_view(), name='stock_search'),
     path('autocomplet', autocomplete_view, name='autocomplete_view'),
    path('', views.index,name='index'),
    path('home', views.index,name='index'),
    
    #  path("register-item", views.register_item, name="register-item"),
     path("user",views.UserListView.as_view()  ,name="user"),
     path("chart",views.user_dashboard  ,name="chart"),
     path("item",views.ItemListView.as_view() , name="item"),
     path("component",views.ComponentListView.as_view() , name="component"),
     path('section', views.SectionListView.as_view(), name='section'),
     path('assignment', views.AssignmentListView.as_view(), name='assignment'),
     path('item-list_for_approval', views.AssignmentListView1.as_view(), name='assignment1'),
     path('report', views.ReportListView.as_view(), name='report'),
     
    #  path('delete', views.delete, name='delete'),
   #create
   
     path('item/create-item', views.ItemCreateView.as_view(),name='create-item'),
     path('assignment/create-component/<str:id>', views.component_create_view,name='create-component'),
     path("user/register", views.UserCreateView.as_view(), name="register"),
     path('section/create-section', views.SectionCreateView.as_view(),name='create-section'),
     path('item/create-assignment/<str:id>', views.AssignmentCreateView.as_view(),name='create-assignment'),
    #  path('save_assignment', views.save_assignment_view,name='save_assignment'),
     path('change_password/', views.change_password, name='change_password'),
     path('password_change_done/', views.password_change_done, name='password_change_done'),
     path('accounts/', include('django.contrib.auth.urls')), 
 path('report/component/<int:item_id>/', views.component_detail_view, name='component_detail'),
# delete
path("delete-user/<str:pk>",views.delete_user ,name="delete-user"),
path('item_delete/<str:pk>',views.delete_item, name='item_delete'),
path("accept-assignment/<str:id>",views.accept_assignment ,name="accept"),
path('conponent-delete/<str:pk>',views.delete_component, name='conponent-delete'),
path("delete-section/<str:pk>",views.delete_section ,name="section-delete"),
path('complete-assignment/<int:pk>/', views.complete_assignment, name='complete'),
path('approve/<int:pk>/', views.approve_assignment, name='approve'),
path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
path('assign_role/<int:pk>/', views.AssignRoleView.as_view(), name='assign_role'),
path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
path('login/', views.custom_login, name='custom_login'),
    # path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read1, name='mark_notification_as_read'),
 path('edit-profile-picture/', views.edit_profile_picture, name='edit_profile_picture'),


# path('mark-notification-as-read/', views.mark_notification_as_read1, name='mark_notification_as_read'),
# path('mark_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
path('message-count_1/', views.get_message_count_1, name='message_count_1'),

 path('send_reset_email/', send_password_reset_email, name='send_password_reset_email'),
    path('password_reset/<uuid:token>/', password_reset, name='password_reset'),
    path('reset_expired/', reset_expired, name='reset_expired'),
    path('stock-item-list/', views.StockItemList.as_view(), name='stock_item_list'),
    path('district-item-list/', views.DistrictItemList.as_view(), name='district_item_list'),
    path('stection-item-list/', views.SectionItemList.as_view(), name='section_item_list'),
    path('engineer-item-status/', views.EngineerItemStatusView.as_view(), name='engineer_item_status'),
    path('stock-item-list/stocks/<int:stock_id>/', views.StockItemDetailView.as_view(), name='stock_item_detail'),
    path('stection-item-list/section/<int:section_id>/', views.SectionItemDetailView.as_view(), name='section_item_detail'),

    # path('engineer/<int:pk>/', views.EngineerItemDetailView.as_view(), name='engineer_item_detail'),
    path('engineer-item-status/engineer/<int:engineer_id>/items/', views.engineer_item_list, name='engineer_item_list'),


]
