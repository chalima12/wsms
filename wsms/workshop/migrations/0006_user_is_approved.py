# Generated by Django 4.2.7 on 2024-03-15 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0005_alter_item_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(auto_created=True, blank=True, default=False, null=True),
        ),
    ]