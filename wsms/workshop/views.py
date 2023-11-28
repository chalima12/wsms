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
from django.views.decorators.http import require_POST
from django.db.models import Count, Q  # Add this line

from .forms import *

from .models import *
from django.contrib.auth import authenticate, login


from workshop import signals  # If signals is a custom module

# You might want to reorganize your import statements based on your project structure
#"ATMSP-3"	"Paper Low Sensor"


# workshop/views.py

# views.py

import plotly.express as px
import pandas as pd
from plotly.offline import plot


# Render the HTML in a Django template
# context = {'chart_html': html_representation}
# return render(request, 'your_template.html', context)


# Include the image in your template?

def user_dashboard(request):
    item_status_counts = Item.objects.values('status').annotate(count=Count('id'))
    df = pd.DataFrame(item_status_counts)

    # Create a pie chart with hover-over labels
    fig = px.pie(df, names='status', values='count',
    hover_data=['count'], labels={'count': 'items'})
    fig.update_traces(marker=dict(colors=['red', 'green', 'yellow']))
    fig.update_layout(title_text='<b>Item Status</b>', title_x=0.5)

    # Convert the Plotly figure to HTML with config option
    html_representation = fig.to_html(full_html=False, config={'displaylogo': False})


    # Fetch data for the user dashboard
    item_count = Item.objects.count()
    user_count = Item.objects.filter(is_valid=True, status="pending").count()
    component_count = Item.objects.filter(is_valid=True, status='Damage').count()
    section_count = Item.objects.filter(is_valid=True, status='completed').count()


     # Fetch items per section counts with status
    section_item_counts = Section.objects.filter(is_valid=True).annotate(
        item_count=Count('sections__id'),
        pending_count=Count('sections__id', filter=Q(sections__status='pending')),
        Damage_count=Count('sections__id', filter=Q(sections__status='Damage')),
        completed_count=Count('sections__id', filter=Q(sections__status='completed')),
    ).values('name', 'item_count', 'pending_count', 'Damage_count', 'completed_count').order_by('id')

    # Create a DataFrame from the queryset
    df = pd.DataFrame(section_item_counts)

    # Create a bar chart using Plotly Express
    fig = px.bar(df, x='name', y=['item_count', 'pending_count', 'Damage_count', 'completed_count'],
                 labels={'value': 'Count', 'variable': 'Status'},
                 
                 color_discrete_map={'item_count': 'blue', 'pending_count': 'yellow', 'Damage_count': 'red', 'completed_count': 'green'})

    # Update layout for better visualization
    fig.update_layout(barmode='group', xaxis_title='Section', yaxis_title='Count')
    fig.update_layout(title_text='<b>Items per Section with Status</b>', title_x=0.5)

    # Convert the figure to HTML
    plot_div = plot(fig, output_type='div', include_plotlyjs=False,config={'displaylogo': False})



    
    section_item_count = Section.objects.filter(is_valid=True).annotate(
        item_count=Count('sections__id'),
        
    ).values('name', 'item_count').order_by('id')
    
    
    
    df = pd.DataFrame(section_item_count)
    fig = px.pie(df, names='name', values='item_count',
                hover_data=['item_count'], labels={'count': 'items'})
    fig.update_traces(marker=dict(colors=['lime', 'Orange', 'purple','blue','pink'])),
    fig.update_layout(title_text='<b>Items per Section</b>', title_x=0.5)

    # Convert the Plotly figure to HTML
    html_representation1 = fig.to_html(full_html=False, config={'displaylogo': False})



    context = {
        'plot_div': plot_div,
        'chart_html': html_representation,
        'chart_html1': html_representation1,
        'user_count': user_count,
        'item_count': item_count,
        'component_count': component_count,
        'section_count': section_count,
    }

    return render(request, 'workshop/home.html', context)
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

    # def form_valid(self, form):
    #     assignment = form.save()
    #     item = assignment.item
    #     item.status = 'pending'
    #     item.engineer = assignment.engineer
    #     item.save()

    #     return super().form_valid(form)
    



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
        user_type = self.request.user.user_type
        

        if user_type == 'Registeror':
            return Item.objects.filter(is_valid=True).order_by('-received_date')
        elif user_type == 'Manager':
            assigned_items = Section.objects.filter(manager=self.request.user, is_valid=True)
            sections_ids = assigned_items.values_list('id', flat=True)
            return Item.objects.filter(Section_id__in=sections_ids, is_valid=True).order_by('-id')
        elif user_type == 'Engineer':
            return Item.objects.filter(engineer=self.request.user, is_valid=True)
            
        else:
            return Item.objects.none()
        
   
class ComponentListView(LoginRequiredMixin, ListView):
    model = Component
    context_object_name = 'components'
    template_name = "workshop/component.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        user_type = self.request.user.user_type

        if user_type == 'Registeror':
            return Component.objects.filter(is_valid=True).order_by('-recived_date')
        elif user_type == 'Engineer':
            assigned_items = Assignments.objects.filter(engineer=self.request.user, is_valid=True)
            assigned_item_ids = assigned_items.values_list('item_id', flat=True)
            return Component.objects.filter(item_id__in=assigned_item_ids, is_valid=True).order_by('-recived_date')
        elif user_type == 'Manager':
            assigned_items = Section.objects.filter(manager=self.request.user, is_valid=True)
            sections_ids = assigned_items.values_list('id', flat=True)
            item_id=Item.objects.filter(Section_id__in=sections_ids, is_valid=True).order_by('-id')
            return Component.objects.filter(item_id__in=item_id, is_valid=True).order_by('-id')
        else:
            return Component.objects.none()
  
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

        if user_type == 'Registeror':
            # If the user is a manager, retrieve all assignments
            return Assignments.objects.filter(is_valid=True).order_by('-id')
        elif user_type == 'Manager':
            assigned_items = Section.objects.filter(manager=self.request.user, is_valid=True)
            sections_ids = assigned_items.values_list('id', flat=True)
            item_id=Item.objects.filter(Section_id__in=sections_ids, is_valid=True).order_by('-id')
            return Assignments.objects.filter(item_id__in=item_id, is_valid=True).order_by('-id')
        else:
        
            # If the user is not a manager, retrieve assignments for the specific engineer
            return Assignments.objects.filter(is_valid=True, engineer=user).order_by('-id')



class ReporttListView(LoginRequiredMixin, ListView):
    model = Assignments
    context_object_name = 'assignments'
    template_name = "workshop/report.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self, start_date, end_date, time_range):
        user = self.request.user
        current_date = timezone.now().date()

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            if time_range == 'daily':
                start_date = current_date
            elif time_range == 'weekly':
                start_date = current_date - timedelta(days=(current_date.weekday() - 4) % 7)
            elif time_range == 'monthly':
                start_date = current_date.replace(day=1)
            elif time_range == 'quarterly':
                quarter_start_month = ((current_date.month - 1) // 3) * 3 + 1
                start_date = current_date.replace(month=quarter_start_month, day=1)
            elif time_range == 'yearly':
                start_date = current_date.replace(month=1, day=1)
            elif time_range == 'all':
                start_date = None

        if start_date is not None:
            queryset = Assignments.objects.filter(
                is_valid=True,
                item__received_date__gte=start_date,
                item__received_date__lte=end_date or current_date
            ).order_by('-id')
        else:
            queryset = Assignments.objects.filter(
                is_valid=True
            ).order_by('-id')



        # Filter by report type
        report_type = self.request.GET.get('report_type', 'all')

        if report_type == 'damage':
            queryset = queryset.filter(
                is_valid=True,
                item__is_maintainable=False
            )
        elif report_type == 'completed':
            queryset = queryset.filter(
                is_valid=True,
                item__status='completed'
            )
        elif report_type == 'remaining':
            queryset = queryset.filter(
                is_valid=True,
                item__status__in=['pending', 'on_progress'],
                item__is_maintainable=True
            )

        # Customize queryset based on user's role
        if user.user_type == 'Registeror':
            # Display all reports for 'Registeror' users
            pass
        elif user.user_type == 'Manager':
            # Display reports related to the manager's section
            queryset = queryset.filter(item__Section__manager=user)
        elif user.user_type == 'Engineer':
            # Display reports where the engineer is assigned
            queryset = queryset.filter(engineer=user)

        return queryset

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        time_range = request.GET.get('time_range', 'daily')

        assignments = self.get_queryset(start_date, end_date, time_range)

        context = {
            'assignments': assignments,
            'time_range': time_range,
            'report_type': request.GET.get('report_type', 'all'),
            'start_date': start_date,
            'end_date': end_date,
        }

        return render(request, self.template_name, context)
    
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
            item.status='Damage'
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




@require_POST


def autocomplete_view(request):
    user_input = request.GET.get('user_input', '')
    
    # Query your Stock model based on the user input
    try:
        stock = Stock.objects.get(name__icontains=user_input)
        stock_id = stock.id  # Replace with the actual field you want to use
    except Stock.DoesNotExist:
        stock_id = None

    return JsonResponse({'stock_id': stock_id})


from django.views import View

class StockSearchView(View):
    def get(self, request, *args, **kwargs):
        input_text = request.GET.get('q', '')
        
        # Query the Stock model to find a match
        stocks = Stock.objects.filter(number__icontains=input_text)
        
        data = [{'id': stock.number, 'text': stock.number} for stock in stocks]

        return JsonResponse({'results': data})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect

User = get_user_model()

def send_password_reset_email(user):
    # Generate a unique reset token and set the expiration time
    user.reset_token = uuid.uuid4()
    user.reset_token_expires_at = timezone.now() + timezone.timedelta(hours=1)
    user.save()

    # Create a reset link using the reverse function to get the URL
    reset_url = reverse('password_reset', kwargs={'token': str(user.reset_token)})

    # Send the reset email
    send_mail(
        'Password Reset',
        f'Click the following link to reset your password: {reset_url}',
        'from@example.com',
        [user.user_name],
        fail_silently=False,
    )

def password_reset(request, token):
    user = get_object_or_404(User, reset_token=token)

    # Check if the reset token has expired
    if user.reset_token_expires_at < timezone.now():
        return render(request, 'workshop/reset_expired.html')

    if request.method == 'POST':
        # Update the user's password and clear the reset token
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expires_at = None
        user.save()

        return HttpResponseRedirect(reverse('login'))

    return render(request, 'workshop/password_reset.html', {'user': user})
def reset_expired(request):
    return render(request, 'workshop/reset_expired.html')