# Generated by Django 4.2.6 on 2023-10-30 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_assignment', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('delete_section', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('delete_component', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('delete_item', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('delete_user', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('add_section', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('add_assignment', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('add_component', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('add_item', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('add_user', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_report', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_section', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_assignment', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_component', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_item', models.BooleanField(auto_created=True, blank=True, default=True, null=True)),
                ('view_user', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('is_admin', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('view_dashboard', models.BooleanField(auto_created=True, blank=True, default=True, null=True)),
                ('is_superuser', models.BooleanField(auto_created=True, blank=True, default=False, null=True)),
                ('is_staff', models.BooleanField(auto_created=True, blank=True, default=True, null=True)),
                ('is_active', models.BooleanField(auto_created=True, default=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_name', models.EmailField(max_length=50, unique=1)),
                ('pass_word', models.CharField(max_length=15)),
                ('user_type', models.CharField(choices=[('Manager', 'manager'), ('Registeror', 'registeror'), ('Engineer', 'Engineer')], default='Engineer')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_right_to_here', models.BooleanField(auto_created=True, default=True)),
                ('is_maintainable', models.BooleanField(auto_created=True, default=True)),
                ('is_accepted', models.BooleanField(auto_created=True, default=False)),
                ('is_valid', models.BooleanField(auto_created=True, default=True)),
                ('status', models.CharField(auto_created=True, choices=[('pending', 'pending'), ('on_prograss', 'On_progress'), ('completed', 'Completed')], default='pending')),
                ('ws_id', models.CharField(max_length=15)),
                ('received_date', models.DateField(auto_now=True)),
                ('stock_id', models.CharField(max_length=15)),
                ('Serial_no', models.CharField(max_length=15)),
                ('delivered_by', models.CharField(max_length=100)),
                ('received_by', models.CharField(max_length=100)),
                ('remark', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('engineer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_valid', models.BooleanField(default=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('read', 'Read')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(auto_created=True, default=True)),
                ('recived_date', models.DateField(auto_now=True)),
                ('stock_id', models.CharField(max_length=15)),
                ('Serial_no', models.CharField(max_length=15)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='workshop.item')),
            ],
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(auto_created=True, default=True)),
                ('remark', models.TextField(blank=True)),
                ('Assigned_date', models.DateField(auto_now=True)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('Section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.section')),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.item')),
            ],
        ),
    ]
