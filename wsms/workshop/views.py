from datetime import datetime, timedelta
from django.views.generic import UpdateView, CreateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_protect

from .forms import *

from .models import *
from django.contrib.auth import authenticate, login


from workshop import signals  # If signals is a custom module

# You might want to reorganize your import statements based on your project structure



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


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "workshop/register.html"
    login_url = 'workshop:custom_login'
    success_url = reverse_lazy('workshop:user')
    success_message = "User successfully created."

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["pass_word"]
        user.set_password(password)
        user.save()
        return super().form_valid(form)

class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "workshop/add-tem.html"
    success_url = reverse_lazy('workshop:item')
    login_url = 'workshop:custom_login'
    success_message = "Item successfully created."

    def form_valid(self, form):
        serial_no = form.cleaned_data['Serial_no']
        count = Item.objects.filter(Serial_no=serial_no).count()
        if count >= 2:
            messages.warning(self.request, f'This item fixed {count} times before may need special attention.')
        return super().form_valid(form)

class ComponentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "workshop/add_component.html"
    login_url = 'workshop:custom_login'
    success_url = reverse_lazy('workshop:assignment')
    success_message = "Component successfully created."

    def get_initial(self):
        initial = super().get_initial()
        ass = Assignments.objects.get(id=self.kwargs['id'])
        item = ass.item
        initial['item'] = item
        return initial

    def form_valid(self, form):
        # Make sure to set the item field before saving
        form.instance.item = self.get_initial()['item']
        return super().form_valid(form)

class SectionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = "workshop/add_section.html"
    login_url = 'workshop:custom_login'
    success_url = reverse_lazy('workshop:section')
    success_message = "Section successfully created."

class AssignmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Assignments
    form_class = AssignmentForm
    template_name = "workshop/Add_assignment.html"
    login_url = 'workshop:custom_login'
    success_url = reverse_lazy('workshop:assignment')
    success_message = "Assignment successfully created."

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


class ItemDetailView(DetailView):
    model = Item
class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = "workshop/user.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        return User.objects.filter(is_active=True, is_admin=False)

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        return render(request, self.template_name, {'user_list': users})

class ItemListView(LoginRequiredMixin,ListView):
    model = Item
    st=Item.status
    context_object_name='items'
    template_name="workshop/item.html"
    login_url='workshop:custom_login'
    # paginate_by = 10 # if pagination is desired
    def get_queryset(self):
    # return only valid item
        return Item.objects.filter(is_valid=True).order_by('id')
   
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
    context_object_name = 'assignments'
    template_name = "workshop/Assignment.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        user = self.request.user
        user_type = user.user_type

        if user_type == 'manager':
            # If the user is a manager, retrieve all assignments
            return Assignments.objects.filter(is_valid=True).order_by('-id')
        else:
            # If the user is not a manager, retrieve assignments for the specific engineer
            return Assignments.objects.filter(is_valid=True, engineer=user).order_by('-id')



class ReporttListView(LoginRequiredMixin, ListView):
    model = Assignments
    context_object_name = 'assignments'
    template_name = "workshop/report.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        time_range = self.request.GET.get('time_range', 'daily')
        current_date = timezone.now().date()

        if time_range == 'daily':
            start_date = current_date
        elif time_range == 'weekly':
            start_date = current_date - timedelta(days=current_date.weekday())
        elif time_range == 'monthly':
            start_date = current_date.replace(day=1)
        else:
            # Handle other cases or set a default behavior
            start_date = current_date

        queryset = Assignments.objects.filter(
            is_valid=True,
            item__received_date__gte=start_date,
            item__received_date__lte=current_date
        ).order_by('-item__received_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_range'] = self.request.GET.get('time_range', 'daily')
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

class AssignRoleView(UpdateView):
    model = User
    context_object_name = 'role'
    template_name = 'workshop/assign_role.html'
    form_class = UserPermissionsForm
    success_url = reverse_lazy('workshop:user')

    def form_valid(self, form):
        # Your existing form_valid logic for assigning the role

        # Add success message
        messages.success(self.request, 'Role assigned successfully.')

        return super().form_valid(form)
@login_required
def get_message_count_1(request):
    
    user_id = request.user
    no_assignment = Notification.objects.filter(engineer=user_id,status='pending').count()
    notify=f'you have { no_assignment } new assignments'

    # Add the following code to remove the badge if the engineer clicks mark as read
    if request.method == 'POST':
        if request.POST.get('mark_as_read'):
            Notification.objects.filter(engineer=user_id,status='read').update(status='read')
            no_assignment = 0
            
            
            
    if no_assignment != 0:
        data = {
            'message_count_1': no_assignment,
            'notify': notify
        }
        return JsonResponse(data)
    return JsonResponse({})



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