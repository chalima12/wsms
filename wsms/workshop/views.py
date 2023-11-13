
import datetime
from workshop import signals
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render
from django.views.generic import (
                                  CreateView,
                                  DetailView,
                                  ListView)
from .models import *
from django.contrib import messages

from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from workshop.models import Assignments
from django.dispatch import Signal
from .import signals
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.http import JsonResponse

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class AssignmentChartView(LoginRequiredMixin,TemplateView):
    template_name = 'workshop/home.html'
    login_url='workshop:custom_login'
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the count of assignments grouped by status
        assignments = Assignments.objects.values('item__Serial_no', 'is_valid').annotate(count=Count('id'))
        # Convert the data into a format that can be used by Chart.js
        item=Item.objects.all().count()
        section=Section.objects.all().count()
        user=User.objects.all().count()
        component=Component.objects.all().count()
        # data = Assignments.objects.values('item__status').annotate(count=Count('item__status'))
        data = Item.objects.values('status').annotate(count=Count('status'))
        users = User.objects.values('user_type').annotate(count=Count('user_type'))
        label3 = [user['user_type'] for user in users]
        count3 = [user['count'] for user in users]
        
        items = Item.objects.values('Serial_no').annotate(count=Count('id'))
        # Convert the data into a format that can be used by Chart.js
        label2 = [item['Serial_no'] for item in items]
        count = [item['count'] for item in items]
        # Add the data to the context
        context['label2'] = label2
        context['count'] = count
        context['label3'] = label3
        context['count3'] = count3
        label = [d['status'] for d in data]
        counts = [d['count'] for d in data]
        labels = []
        valid_counts = []
        invalid_counts = []
        for assignment in assignments:
            labels.append(assignment['item__Serial_no'])
            if assignment['is_valid']:
                valid_counts.append(assignment['count'])
                invalid_counts.append(0)
            else:
                valid_counts.append(0)
                invalid_counts.append(assignment['count'])
        # Add the data to the context
        context['item'] = item
        context['section'] = section
        context['user'] = user
        context['component'] = component
        context['labels'] = labels
        context['label'] = label
        context['counts'] = counts
        context['valid_counts'] = valid_counts
        context['invalid_counts'] = invalid_counts
        
        context['status_counts'] = counts
        return context    
        
from django.shortcuts import render
from django.db.models import Count
from .models import Assignments, Item, User, Component, Section

@login_required(login_url='workshop:custom_login')
def assignment_chart_view(request):
    # Get the count of assignments grouped by status
    assignments = Item.objects.values('Serial_no', 'is_accepted').annotate(count=Count('id'))

    item = Item.objects.all().count()
    section = Section.objects.all().count()
    user = User.objects.all().count()
    component = Component.objects.all().count()

    data = Item.objects.values('status').annotate(count=Count('status'))
    users = User.objects.values('user_type').annotate(count=Count('user_type'))

    label3 = [user['user_type'] for user in users]
    count3 = [user['count'] for user in users]

    items = Item.objects.values('Serial_no').annotate(count=Count('id'))
    label2 = [item['Serial_no'] for item in items]
    count = [item['count'] for item in items]

    label = [d['status'] for d in data]
    counts = [d['count'] for d in data]

    labels = []
    valid_counts = []
    invalid_counts = []

    for assignment in assignments:
        labels.append(assignment['Serial_no'])
        if assignment['is_accepted']:
            valid_counts.append(assignment['count'])
            invalid_counts.append(0)
        else:
            valid_counts.append(0)
            invalid_counts.append(assignment['count'])

    context = {
        'item': item,
        'section': section,
        'user': user,
        'component': component,
        'labels': labels,
        'label': label,
        'counts': counts,
        'valid_counts': valid_counts,
        'invalid_counts': invalid_counts,
        'label2': label2,
        'count': count,
        'label3': label3,
        'count3': count3,
    }

    return render(request, 'workshop/home.html', context)

@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chart')  # Replace 'desired_page' with the URL name or path of the page you want to redirect to after login
        else:
            error_message = 'Invalid username or password'
            return render(request, 'workshop/login.html', {'error_message': error_message})
    else:
        return render(request, 'workshop/login.html')

def index(request_iter):
    return  render(request_iter,'workshop/index.html')

from django.shortcuts import render

def notifications_view(request):
    user_id = request.user
    notifications = Notification.objects.filter(engineer=user_id,status='pending')
    count=notifications.count()
    context = {'notifications': notifications,'count': count}
    return render(request, 'notifications.html', context)

class UserCreateView(LoginRequiredMixin,CreateView):
    model = User
    # fields='__all__'
    form_class=UserForm
    template_name = "workshop/register.html"
    login_url='workshop:custom_login'

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

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "workshop/add-tem.html"
    success_url = reverse_lazy('workshop:item')
    login_url = 'workshop:custom_login'
    

    def form_valid(self, form):
        # Check if there are already 2 or more items with the same serial number
        serial_no = form.cleaned_data['Serial_no']
        count = Item.objects.filter(Serial_no=serial_no).count()
        if count >= 2:
            messages.warning(self.request, f'This item fixed {count} times before may need spetial attentions.')
        return super().form_valid(form)
class ComponentCreateView(LoginRequiredMixin,CreateView):
    model = Component
    form_class=ComponentForm
    template_name = "workshop/add_component.html"
    login_url='workshop:custom_login'
    success_url = reverse_lazy('workshop:assignment')
    def get_initial(self):
        # get the initial data for the form
        initial = super().get_initial()
        # get the item object from the url parameter
        ass = Assignments.objects.get(id=self.kwargs['id'])
        item=ass.item
        # set the initial value for the item field
        initial['item'] = item
        return initial
    


class SectionCreateView(LoginRequiredMixin,CreateView):
    model = Section
    form_class=SectionForm
    template_name = "workshop/add_section.html"
    login_url='workshop:custom_login'
    success_url = reverse_lazy('workshop:section')




class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignments
    form_class = AssignmentForm
    template_name = "workshop/Add_assignment.html"
    login_url = 'workshop:custom_login'
    success_url = reverse_lazy('workshop:assignment')
    

    def get_initial(self):
        initial = super().get_initial()
        item = Item.objects.get(id=self.kwargs['id'])
        initial['item'] = item
        return initial

    def form_valid(self, form):
        assignment = form.save()
        item = assignment.item
        item.status = 'on_progress'
        item.engineer = assignment.engineer
        item.save()

        return super().form_valid(form)
    



# View for sending notifications


@login_required
def get_notifications(request):
    user_id = request.user.id

    notifications = Notification.objects.filter(engineer=user_id).order_by('-created_at')
    unread_count = notifications.filter(status='pending').count()

    notifications_data = [
        {
            'id': notification.id,
            'message': notification.message,
            'link': notification.link,
            'status': notification.status,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for notification in notifications
    ]

    data = {
        'notifications': notifications_data,
        'unread_count': unread_count,
    }

    return JsonResponse(data)




from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def mark_notification_as_read(request, notification_id):
    try:
        # Get the notification object with the specified ID or return a 404 error if not found
        notification = get_object_or_404(Notification, pk=notification_id)

        # Mark the notification as 'read'
        notification.status = 'read'
        notification.save()

        # Check if there are any remaining unread notifications
        unread_notifications = Notification.objects.filter(status='pending')

        # Determine whether to hide the dropdown based on the presence of unread notifications
        hide_dropdown = not unread_notifications.exists()

        # Prepare the JSON response
        response_data = {
            'success': True,
            'hideDropdown': hide_dropdown
        }

        return JsonResponse(response_data)

    except Notification.DoesNotExist:
        # Handle the case where the notification ID is invalid
        response_data = {
            'success': False,
            'error': 'Notification not found'
        }

        return JsonResponse(response_data)


class ItemDetailView(DetailView):
    model = Item
class UserListView(LoginRequiredMixin,ListView):
    model = User

    context_object_name='users'
    template_name="workshop/user.html"
    login_url='workshop:custom_login'
    
    def get_queryset(self):
    
# return only active users
        return User.objects.filter(is_active=True,is_admin=False)


class ItemListView(LoginRequiredMixin,ListView):
    model = Item
    st=Item.status
    context_object_name='items'
    template_name="workshop/item.html"
    login_url='workshop:custom_login'
    # paginate_by = 10 # if pagination is desired
    def get_queryset(self):
    # return only valid item
        return Item.objects.filter(is_valid=True)
   
class ComponentListView(LoginRequiredMixin,ListView):
    model = Component
    context_object_name='components'
    template_name="workshop/component.html"
    login_url='workshop:custom_login'
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only valid item
        return Component.objects.filter(is_valid=True)

class SectionListView(LoginRequiredMixin,ListView):
    model = Section
    context_object_name='sections'
    template_name="workshop/section.html"
    login_url='workshop:custom_login'
    # paginate_by = 4 # if pagination is desired
    def get_queryset(self):
# return only valid section
        return Section.objects.filter(is_valid=True)
class AssignmentListView(LoginRequiredMixin,ListView):
    model = Assignments
    
    context_object_name='assignments'
    template_name="workshop/Assignment.html"
    login_url='workshop:custom_login'
    def get_queryset(self):
        
        return Assignments.objects.filter(is_valid=True, engineer=self.request.user)
    

class ReporttListView(LoginRequiredMixin, ListView):
    model = Assignments
    context_object_name = 'assignments'
    template_name = "workshop/report.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        return Assignments.objects.filter(is_valid=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignments = context['assignments']

        for assignment in assignments:
            components = Component.objects.filter(item=assignment.item)
            assignment.components = components

        return context
@login_required(login_url='/login')
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
@login_required(login_url='/login')

def delete_item(request,pk):
    item=Item.objects.get(id=pk)
    if request.method=='POST':
        item.is_valid=False
        item.save()
        messages.success(request,  f'user {item.Serial_no} has been deactivated successfully.')
        return redirect('/item')
    context={'item':item}
    return render(request,'workshop/delete-item.html',context)

@login_required(login_url='/login')

def delete_component(request,pk):
    component=Component.objects.get(id=pk)
    if request.method=='POST':
        component.is_valid=False
        component.save()
        messages.success(request,  f'Componente {component.Serial_no} has been deactivated successfully.')
        return redirect('/component')
    context={'component':component}
    return render(request,'workshop/delete-item.html',context)

@login_required(login_url='/login')

def delete_section(request,pk):
    section=Section.objects.get(id=pk)
    if request.method=='POST':
        section.is_valid=False
        section.save()
        messages.success(request,  f'Section {section.name} has been deactivated successfully.')
        return redirect('/section')
    context={'section':section}
    return render(request,'workshop/delete-item.html',context)


@login_required(login_url='/login')
def delete_assignment(request,pk):
    assign=Assignments.objects.get(id=pk)
    
    if request.method=='POST':
        assign.is_valid=False
        assign.save()
        messages.success(request,  f'user {assign.id} has been deactivated successfully.')
        return redirect('/assignment')
    context={'assign':assign}
    return render(request,'workshop/delete-assignment.html',context)

from django.shortcuts import get_object_or_404

@login_required(login_url='/login')
def accept_assignment(request, id):
    assign = get_object_or_404(Assignments, id=id)
    item = assign.item

    # Retrieve the associated Notification
    notification = Notification.objects.filter(assignment=assign).first()

    if request.method == 'POST':
        item.is_accepted = True
        item.save()

        # Update the status of the associated Notification
        if notification:
            notification.mark_as_read()

        messages.success(request, f'Assignment {assign.id} has been accepted successfully.')
        return redirect('/assignment')

    context = {'assign': assign}
    return render(request, 'workshop/accept_form.html', context)

@login_required(login_url='/login')

def complete_assignment(request, pk):
    assign = Assignments.objects.get(id=pk)
    item = assign.item
    if request.method == 'POST':
        item.status = 'completed'
        assign.completed_date = timezone.now()
        assign.save()
        if 'is_maintainable' in request.POST:
            item.is_maintainable = True
        else:
            item.is_maintainable = False
        if 'is_right_to_here' in request.POST:
            item.is_right_to_here = True
        else:
            item.is_right_to_here = False
        
        item.comment = request.POST.get('comment', '')
        item.save()
        messages.success(request, f'Assignment {assign.id} has been completed successfully.')
        return redirect('/assignment')
    context = {'assign': assign}
    return render(request, 'workshop/complete.html', context)


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

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from .forms import CustomPasswordChangeForm  # Import your custom form

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)  # Use the custom form
        if form.is_valid():
            messages.success(request, 'Password changed Successfully')
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            return redirect('workshop:chart')
    else:
        form = CustomPasswordChangeForm(request.user)  # Use the custom form
    return render(request, 'workshop/change-password/change_password.html', {'form': form})


def password_change_done(request):
    return render(request, 'workshop/change-password/password_change_done.html')


from django.views.generic import UpdateView

from .forms import UserPermissionsForm

class AssignRoleView(UpdateView):
    model = User
    template_name='workshop/assign_role.html'
    form_class = UserPermissionsForm
    success_url = reverse_lazy('workshop:user')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['assigned_user'] = self.object
    #     return context


from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification

def get_message_count(request):
    user = request.user
    unread_notifications = Notification.objects.filter(user=user, status='pending').count()
    
    data = {
        'message_count': unread_notifications,
    }
    
    return JsonResponse(data)

# def mark_notification_as_read(request, notification_id):
#     try:
#         notification = Notification.objects.get(id=notification_id, user=request.user)
#         notification.mark_as_read()
#         return JsonResponse({'success': 'Notification marked as read.'})
#     except Notification.DoesNotExist:
#         return JsonResponse({'error': 'Notification not found.'}, status=400)





@login_required
def mark_notification_as_read1(request, notification_id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=notification_id, status='pending')
            print('Received Notification ID:', notification_id)  # Check if the correct ID is being received
            notification.status = 'read'
            notification.save()
            print('Notification marked as read:', notification_id)  # Check if it's successfully marked as read
            return JsonResponse({'status': 'read'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found or already marked as read'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




@login_required
def get_message_count_1(request):
    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=-1)
    user_id = request.user
    no_assignment = Notification.objects.filter(engineer=user_id,status='pending').count()
    notify=f'you have { no_assignment } new assignments'

    # Add the following code to remove the badge if the engineer clicks mark as read
    if request.method == 'POST':
        if request.POST.get('mark_as_read'):
            Notification.objects.filter(engineer=user_id,status='read').update(status='read')
            no_assignment = 0
            
            
            
    if no_assignment!=0:
        data = {
            'message_count_1': no_assignment,
            'notify': notify
        }
    return JsonResponse(data)



# views.py
from django.contrib import messages

def edit_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Update the profile picture behind the scenes
            # without the user's awareness
            form.save()
            messages.success(request, 'Profile has updated successfully.')
            return redirect('workshop:user')  # Redirect to the user's profile page
        else:
            messages.error(request, 'Profile picture update failed. Please try again.')

    else:
        form = ProfilePictureForm(instance=request.user)

    return render(request, 'workshop/edit_profile_picture.html', {'form': form})

# views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, engineer=request.user)
    notification.mark_as_read()
    return redirect('notifications_list')  # Redirect to the notifications list or wherever you display notifications



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