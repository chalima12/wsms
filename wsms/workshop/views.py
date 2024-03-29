from django.views.generic import UpdateView, CreateView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login, get_user_model
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.forms import BaseFormSet, inlineformset_factory, modelformset_factory
from .forms import *
from .models import *
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.offline import plot
from datetime import datetime, timedelta
from django.contrib import messages



@login_required(login_url='workshop:custom_login')

def item_status_chart(request):
    # Get start_date and end_date from the query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialize items as an empty queryset

    items = Item.objects.all()

    # Retrieve items based on the selected date range
    if start_date and end_date:
        items = items.filter(received_date__range=[start_date, end_date])

    # Create a DataFrame from the queryset
    data = {
        'Section': [item.Section.name for item in items],
        'Status': [item.status for item in items],
    }
    df = pd.DataFrame(data)

    # Perform data aggregation to get the sum of counts for each status in each section
    grouped_df = df.groupby(['Section', 'Status']).size().reset_index(name='Count')
    # Define color map for each status
    color_discrete_map = {
        'Damage': 'red',
        'completed': 'green',
        'pending': 'yellow',
    }

    # Create a vertical bar chart using Plotly with barmode='group' and custom colors
    fig = px.bar(
        grouped_df,
        x='Section',
        y='Count',
        color='Status',
        title='Item Status per Section',
        barmode='group',
        color_discrete_map=color_discrete_map,
        labels={'Count': 'Item Count'},  # Optional label customization
    )
    total_count_per_section = df.groupby('Section')['Status'].count().reset_index(name='Total Count')
    fig.add_trace(
            go.Bar(
                x=total_count_per_section['Section'],
                y=total_count_per_section['Total Count'],
                name='Total Items',
                marker_color='blue',  # Set your desired color for the total count
            ))
    

    # Convert the chart to HTML
    chart_html = fig.to_html(full_html=False,config={'displaylogo': False})

    return render(
        request,
        'workshop/status_chart.html',
        {
            'plot3_html': chart_html,
            'start_date': start_date,
            'end_date': end_date,
        },
    )


# Include the image in your template?

@login_required
def analysis_view(request):
    user = request.user

    # Filter items based on user type
    if user.user_type == 'Registeror':
        items = Item.objects.all()
    elif user.user_type == 'Manager':
        items = Item.objects.filter(Section__manager=user)
    elif user.user_type == 'Engineer':
        items = Item.objects.filter(engineer=user)

    # Filter items based on the selected time range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        items = items.filter(received_date__range=[start_date, end_date])

    # Create a DataFrame for analysis
    data = {
        'Status': items.values_list('status', flat=True),
        'Section': items.values_list('Section__name', flat=True),
    }
    df = pd.DataFrame(data)
    color_discrete_map = {
        'Damage': 'red',
        'completed': 'green',
        'pending': 'yellow',
    }

    # Generate Pie Chart of Total Items by Status
    fig1 = px.pie(
        df,
        names='Status',
        title='Total Items by Status',
        color_discrete_map=color_discrete_map,
    )

    fig1.update_traces(
        hoverinfo='label+percent+name',
        hovertemplate='%{label}: %{value} items',
    )

    # Generate Pie Chart of Total Items in Each Section
    fig2 = px.pie(
        df,
        names='Section',
        title='Total Items in Each Section',
        color_discrete_map=color_discrete_map,
    )

    fig2.update_traces(
        hoverinfo='label+percent+name',
        hovertemplate='%{label}: %{value} items',
    )

    # Generate Vertical Bar Chart of Status of Items in Each Section
    fig3 = px.bar(
        df.groupby(['Section', 'Status']).size().reset_index(name='Count'),
        x='Section',
        y='Count',
        color='Status',
        barmode='group',
        title='Status of Items in Each Section',
        color_discrete_map=color_discrete_map,
    )

    # Add trace for total count per section
    total_count_per_section = df.groupby('Section')['Status'].count().reset_index(name='Total Count')
    fig3.add_trace(
        go.Bar(
            x=total_count_per_section['Section'],
            y=total_count_per_section['Total Count'],
            name='Total Items',
            marker_color='blue',  # Set your desired color for the total count
        )
    )
    # Display Serial numbers and their total count in a Plotly vertical bar chart
    items_count = Item.objects.values('Serial_no').annotate(count=models.Count('Serial_no'))
    filtered_items = {item['Serial_no']: item['count'] for item in items_count if item['count'] > 2}

    # Create a vertical bar chart
    trace = go.Bar(
        x=list(filtered_items.keys()),  # Serial numbers on x-axis
        y=list(filtered_items.values()),  # Total count on y-axis
        text=[f"Repeation Time: {count}" for count in filtered_items.values()],
        orientation='v'  # Set orientation to 'v' for vertical bars
    )

    layout = go.Layout(title='Total Count of Items Registered More Than Two Times', xaxis_title='Serial Number', yaxis_title='Total Count')

    fig4 = go.Figure(data=[trace], layout=layout)




    # Convert plots to HTML
    plot1_html = fig1.to_html(full_html=False, config={'displaylogo': False})
    plot2_html = fig2.to_html(full_html=False, config={'displaylogo': False})
    plot3_html = fig3.to_html(full_html=False, config={'displaylogo': False})
    plot4_html = fig4.to_html(full_html=False, config={'displaylogo': False})

    return render(
        request,
        'workshop/data_analysis.html',
        {
            'plot1_html': plot1_html,
            'plot2_html': plot2_html,
            'plot3_html': plot3_html,
            'plot4_html': plot4_html,
            'start_date': start_date,
            'end_date': end_date,
        },
    )


def user_dashboard(request):
    user = request.user
     # Filter items based on user type
    if user.user_type == 'Registeror':
        items = Item.objects.all()
    elif user.user_type == 'Manager':
        items = Item.objects.filter(Section__manager=user)
    elif user.user_type == 'Engineer':
        items = Item.objects.filter(engineer=user)

   
    item_status_counts = items.values('status').annotate(count=Count('status'))

    # Check if 'status' key exists in the queryset
    if item_status_counts.exists():
        df = pd.DataFrame(item_status_counts)

        # Order the dataframe based on the desired sequence
        status_order = ['pending', 'completed', 'Damage']
        df['status'] = pd.Categorical(df['status'], categories=status_order, ordered=True)
        df = df.sort_values('status')

        # Create a pie chart with hover-over labels
        fig = px.pie(df, names='status', values='count', hover_data=['count'], labels={'count': 'items'})
        fig.update_traces(marker=dict(colors=['yellow', 'green', 'red']))


        # Convert the Plotly figure to HTML with config option
        html_representation = fig.to_html(full_html=False, config={'displaylogo': False})

    else:
        # If 'status' key doesn't exist, set html_representation to None or an appropriate value
        html_representation = None
    item_count = items.filter( is_valid=True).count()
    user_count = items.filter(is_valid=True, status="pending").count()
    component_count = items.filter(is_valid=True, status='Damage').count()
    section_count = items.filter(is_valid=True, status='completed').count()

    # Fetch data for the user dashboard
        # Get today's date
    today = timezone.now().date()
    current_date = timezone.now().strftime("%Y-%m-%d")


    # Query the data
    Today_item_count = items.filter(received_date=today, is_valid=True).count()
    today_pending = items.filter(is_valid=True, status="pending").count()
    today_damage = items.filter(completed_date=today,is_valid=True, status='Damage').count()
    today_completed = items.filter(completed_date=today, is_valid=True, status='completed').count()

    # Create DataFrame
    data = {
        'Category': ['New Item', 'Pending', 'Damage(TODAY)', 'Completed(TODAY)'],
        'Count': [Today_item_count, today_pending, today_damage, today_completed]
    }

    # Convert to DataFrame and ensure 'Category' column is of string type
    df = pd.DataFrame(data)
    custom_colors = {
        'New Item': 'rgb(31, 119, 180)',
        'Pending': 'rgb(255, 255, 0)',
        'Damage(TODAY)': 'rgb(255, 0, 0)',
        'Completed(TODAY)': 'rgb(0, 255, 0)'
    }

    df['Category'] = df['Category'].astype(str)

    # Custom colors
   
    # Create pie chart
    fig = px.bar(df, x='Category', y='Count', title= current_date,
             color='Category', color_discrete_map=custom_colors)

# Convert Plotly figure to HTML
    plot_div1 = fig.to_html(full_html=False,config={'displaylogo': False})



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

    # Define custom colors
    custom_colors = ['lime', 'orange', 'purple', 'blue', 'pink']

    fig = px.pie(
        df,
        names='name',
        values='item_count',
        hover_data=['item_count'],
        title='<b>Items per Section</b>',
        color_discrete_sequence=custom_colors,
    )

    # Update the traces to display the count number instead of percentage
    fig.update_traces(textinfo='value', textfont_size=12)

    # Set the title position using update_layout
    fig.update_layout(title_x=0.5)

    # Convert the Plotly figure to HTML
    html_representation1 = fig.to_html(full_html=False, config={'displaylogo': False})

    context = {
        'plot_div': plot_div,
        'chart_html': plot_div1,
        'chart_html1': html_representation,
        'user_count': user_count,
        'item_count': item_count,
        'component_count': component_count,
        'section_count': section_count,
        'Today_item':Today_item_count,
        'Today_completed':today_completed,
        'Today_damage':today_damage,
    }

    return render(request, 'workshop/home.html', context)

from django.shortcuts import redirect

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_wh:  # Assuming 'is_wh' is the attribute indicating whether the user is a warehouse manager
                return redirect('/item-list_for_approval')  # Redirect to the desired page if the user is a warehouse manager
            else:
                return redirect('/chart')  # Redirect to '/chart' if the user is not a warehouse manager
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
    
from django.contrib import messages

def component_create_view(request, id):
    assignment = get_object_or_404(Assignments, id=id)
    item = assignment.item

    ComponentFormSet = modelformset_factory(
        Component,
        form=ComponentForm,
        extra=10
    )

    if request.method == 'POST':
        formset = ComponentFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.item = item
                instance.save()
            messages.success(request, "Components successfully created.")
            return redirect(reverse('workshop:assignment'))
        else:
            messages.error(request, "Error occurred while creating components.")
    else:
        formset = ComponentFormSet(queryset=Component.objects.none())

    context = {
        'formset': formset,
        'item': item,
    }

    return render(request, 'workshop/add_component.html', context)


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
        item.assigned=True
        item.engineer = assignment.engineer
        item.save()

        return super().form_valid(form)
    


class ItemDetailView(DetailView):
    model = Item
class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = "workshop/user.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('-id')

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
            return Item.objects.filter(is_valid=True).order_by('-id')
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
            return Component.objects.filter(is_valid=True).order_by('-id')
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
        
class AssignmentListView1(LoginRequiredMixin,ListView):
    model = Item
    context_object_name = 'assignments'
    template_name = "workshop/Assignment1.html"
    login_url = 'workshop:custom_login'

    def get_queryset(self):
       
        
            # If the user is not a manager, retrieve assignments for the specific engineer
            return Item.objects.filter(is_valid=True,is_approved=False, status='completed').order_by('-completed_date')



@login_required
def report_list_view(request):
    user = request.user
    current_date = timezone.now().date()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    time_range = request.GET.get('time_range', 'all')
    selected_section = request.GET.get('section', 'all')

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
        queryset = Item.objects.filter(
            received_date__gte=start_date,
            received_date__lte=end_date or current_date,
            is_valid=True
        ).order_by('-id')
    else:
        queryset = Item.objects.filter(
            is_valid=True
        ).order_by('-id')

    # Additional filters based on report_type
    report_type = request.GET.get('report_type', 'all')

    if report_type == 'damage':
        queryset = queryset.filter(
            is_valid=True,
            status='Damage'
        )
    elif report_type == 'completed':
        queryset = queryset.filter(
            is_valid=True,
            status='completed'
        )
    elif report_type == 'remaining':
        queryset = queryset.filter(
            is_valid=True,
            status='pending'
        )

    if selected_section != 'all':
        queryset = queryset.filter(Section__id=selected_section)

    # Customize queryset based on user's role
    if user.user_type == 'Registeror':
        pass
    elif user.user_type == 'Manager':
        queryset = queryset.filter(Section__manager=user)
    elif user.user_type == 'Engineer':
        queryset = queryset.filter(engineer=user)

    queryset = queryset.prefetch_related('components')  # Prefetch related components for performance

    context = {
        'assignments': queryset,
        'time_range': request.GET.get('time_range', 'all'),
        'report_type': request.GET.get('report_type', 'all'),
        'start_date': request.GET.get('start_date'),
        'end_date': request.GET.get('end_date'),
        'sections': Section.objects.filter(is_valid=True),
        'selected_section': request.GET.get('section', 'all')
    }

    selected_section_name = None
    if context['selected_section'] != 'all':
        selected_section_name = Section.objects.get(pk=context['selected_section']).name
    context['selected_section_name'] = selected_section_name

    return render(request, 'workshop/report.html', context)









from django.shortcuts import render
from .models import Component

def component_detail_view(request, item_id):
    item_components = Component.objects.filter(item_id=item_id,is_valid=True)
    return render(request, 'workshop/component_detail.html', {'item_components': item_components})



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

# activate Item
@login_required(login_url='/login')

def activate_item(request,pk):
    item=Item.objects.get(id=pk)
    if request.method=='POST':
        item.is_valid=True
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
        messages.success(request,  f'Componente {component.id} has been deactivated successfully.')
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
        item.completed_date = assign.completed_date
        assign.save()
        
        # Check if the checkbox is checked
        if request.POST.get('is_damage') == 'on':
            item.is_damage = True
            item.status = 'Damage'
        else:
            item.is_damage = False
            
        # Check if the checkbox is checked
        if request.POST.get('is_maintainable_onfield') == 'on':
            item.is_maintainable_onfield = True
        else:
            item.is_maintainable_onfield = False
        
        item.comment = request.POST.get('comment', '')
        item.save()
        messages.success(request, f'Assignment {assign.id} has been completed successfully.')
        return redirect('/assignment')


from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item

def approve_assignment(request, pk):
    if request.method == 'POST':
        item = Item.objects.get(pk=pk)

        # Check if the checkbox is checked
        if request.POST.get('is_damage') == 'on':
            item.is_approved = True
        else:
            item.is_approved = False

        item.wh_comment = request.POST.get('comment', '')
        item.save()
        
        messages.success(request, f'Assignment {item.id} has been approved successfully.')
        return redirect('/item-list_for_approval')

    else:
        # Handle GET request
        # You may want to handle GET requests differently, e.g., show a form
        pass






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
            return redirect('workshop:index')  # Redirect to the user's profile page
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


from django.db.models import Count, Sum, Case, When, IntegerField


class StockItemList(ListView):
    model = Stock
    template_name = 'workshop/stock_item_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)  # Default to one month of data

        # Override default dates if provided in the URL parameters
        start_date_param = self.request.GET.get('start_date')
        end_date_param = self.request.GET.get('end_date')

        if start_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()

        if end_date_param:
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()

        queryset = Stock.objects.annotate(
            total_items=Count('stocks'),
            completed_items=Sum(Case(
                When(stocks__status='completed', stocks__received_date__range=(start_date, end_date), then=1),
                default=0,
                output_field=IntegerField()
            )),
            damage_items=Sum(Case(
                When(stocks__status='Damage', stocks__received_date__range=(start_date, end_date), then=1),
                default=0,
                output_field=IntegerField()
            )),
            pending_items=Sum(Case(
                When(stocks__status='pending', stocks__received_date__range=(start_date, end_date), then=1),
                default=0,
                output_field=IntegerField()
            )),
        ).filter(total_items__gt=0)  # Filter out stocks with zero items

        return queryset
from django.db.models import Q

class DistrictItemList(ListView):
    model = District
    template_name = 'workshop/district_item_list.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)  # Default to one month of data

        # Override default dates if provided in the URL parameters
        start_date_param = self.request.GET.get('start_date')
        end_date_param = self.request.GET.get('end_date')

        if start_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()

        if end_date_param:
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()

        queryset = District.objects.annotate(
            total_items=Count('districts'),
            completed_items=Sum(Case(
                When(Q(districts__status='completed') & Q(districts__received_date__range=(start_date, end_date)), then=1),
                default=0,
                output_field=IntegerField()
            )),
            damage_items=Sum(Case(
                When(Q(districts__status='Damage') & Q(districts__received_date__range=(start_date, end_date)), then=1),
                default=0,
                output_field=IntegerField()
            )),
            pending_items=Sum(Case(
                When(Q(districts__status='pending') & Q(districts__received_date__range=(start_date, end_date)), then=1),
                default=0,
                output_field=IntegerField()
            )),
        ).filter(total_items__gt=0)  # Filter out stocks with zero items

        return queryset

    

class SectionItemList(ListView):
    model = Section
    template_name = 'workshop/section_item_list.html'
    context_object_name = 'sections'

    def get_week_boundaries(self, date):
        # Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
        weekday = date.weekday()

        # Calculate the start date of the week (Monday)
        start_date = date - timedelta(days=weekday)

        # Calculate the end date of the week (Sunday)
        end_date = start_date + timedelta(days=6)

        return start_date, end_date

    def get_queryset(self):
    # Get current date and calculate boundaries for current week
        end_date = datetime.now().date()
        start_date, end_date = self.get_week_boundaries(end_date)

        # Query for sections with annotations for pending items for current week and previous week
        queryset = Section.objects.annotate(
            total_items=Count('sections'),
            completed_items=Count('sections', filter=Q(sections__status='completed', sections__completed_date__range=(start_date, end_date))),
            damage_items=Count('sections', filter=Q(sections__status='Damage', sections__completed_date__range=(start_date, end_date))),
            pending_items_current_week=Count('sections', filter=Q(sections__status='pending', sections__received_date__range=(start_date, end_date))),
            pending_items_prev_week=Count('sections', filter=Q(sections__status='pending', sections__received_date__lt=start_date)),
        ).filter(total_items__gt=0)  # Exclude sections with zero items

        return queryset




class StockItemDetailView(ListView):
    model = Item
    template_name = 'workshop/stock_item_detail.html'
    context_object_name = 'items'

    def get_queryset(self):
        stock_id = self.kwargs['stock_id']
        stock = get_object_or_404(Stock, id=stock_id)

        # Get the start and end dates from the query parameters of StockListView
        start_date_param = self.request.GET.get('start_date')
        end_date_param = self.request.GET.get('end_date')

        # If the parameters are not provided, use the default one month range
        if start_date_param and end_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()
        else:
            # Assuming the items are related to the stock through the reverse relation 'stocks'
            first_item = stock.stocks.first()
            start_date = first_item.received_date if first_item else datetime.now().date()
            end_date = start_date + timedelta(days=365)

        # Filter items based on stock and date range
        queryset = Item.objects.filter(stock_id=stock_id, received_date__range=(start_date, end_date))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass stock information to the template
        stock_id = self.kwargs['stock_id']
        stock = get_object_or_404(Stock, id=stock_id)
        context['stock'] = stock
        # Assuming the items are related to the stock through the reverse relation 'stocks'
        context['start_date'] = stock.stocks.first().received_date if stock.stocks.first() else datetime.now().date()
        context['end_date'] = context['start_date'] + timedelta(days=365)  # Default one month range

        return context


class SectionItemDetailView(ListView):
    model = Item
    template_name = 'workshop/section_item_detail.html'
    context_object_name = 'items'

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        section = get_object_or_404(Section, id=section_id)

          # Get the start and end dates from the query parameters of StockListView
        start_date_param = self.request.GET.get('start_date')
        end_date_param = self.request.GET.get('end_date')

        # If the parameters are not provided, use the default one month range
        if start_date_param and end_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()
        else:
            # Assuming the items are related to the stock through the reverse relation 'stocks'
            first_item = section.sections.first()
            start_date = first_item.received_date if first_item else datetime.now().date()
            end_date = start_date + timedelta(days=365)

        # Filter items based on section and date range
        queryset = Item.objects.filter(Section=section, received_date__range=(start_date, end_date))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass section information to the template
        section_id = self.kwargs['section_id']
        section = get_object_or_404(Section, id=section_id)

        # Use the current date as the default start date
        default_start_date = datetime.now().date()

        # Get the start and end dates from the query parameters
        start_date_param = self.request.GET.get('start_date')
        end_date_param = self.request.GET.get('end_date')

        # If start_date_param is provided, try to parse it; otherwise, use the default_start_date
        context['start_date'] = (
            datetime.strptime(start_date_param, '%Y-%m-%d').date()
            if start_date_param
            else default_start_date
        )

        # If end_date_param is provided, try to parse it; otherwise, use the default_start_date + 365 days
        context['end_date'] = (
            datetime.strptime(end_date_param, '%Y-%m-%d').date()
            if end_date_param
            else context['start_date'] + timedelta(days=365)
        )

        context['section'] = section

        return context


class EngineerItemStatusView(TemplateView):
    template_name = 'workshop/engineer_item_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Default to one month ago for start_date and today for end_date
        default_start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        default_end_date = datetime.now().strftime('%Y-%m-%d')

        start_date = self.request.GET.get('start_date', default_start_date)
        end_date = self.request.GET.get('end_date', default_end_date)

        # Annotate the number of items per engineer and per status within the specified date range
        engineer_items = Item.objects.filter(
            engineer__isnull=False,
            received_date__range=(start_date, end_date)
        ).values(
            'engineer__id', 'engineer__first_name', 'engineer__last_name'
        ).annotate(
            total_items=Count('id'),
            pending_items=Count('id', filter=Q(status='pending')),
            damage_items=Count('id', filter=Q(status='Damage')),
            completed_items=Count('id', filter=Q(status='completed')),
        )

        context['engineer_items'] = engineer_items
        context['default_start_date'] = default_start_date
        context['default_end_date'] = default_end_date
        return context




def engineer_item_list(request, engineer_id):
    engineer = User.objects.get(pk=engineer_id)

    # Get start and end dates from the request parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Default to the data of one week if start or end date is not provided
    if not start_date_str:
        # Calculate the start date as the current date minus seven days
        start_date = timezone.now().date() - timedelta(days=365)
    else:
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()

    if not end_date_str:
        # Default to the current date if end date is not provided
        end_date = timezone.now().date()
    else:
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Filter items based on the date range
    items = Item.objects.filter(
        engineer=engineer,
        received_date__range=(start_date, end_date)
    )

    context = {
        'engineer': engineer,
        'items': items,
        'start_date': start_date,
        'end_date': end_date,
    }
    

    return render(request, 'workshop/engineer_item_detail.html', context)
