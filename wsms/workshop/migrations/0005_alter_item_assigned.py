# Generated by Django 4.2.7 on 2023-11-22 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_rename_is_assigned_item_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='assigned',
            field=models.BooleanField(auto_created=True, default=False),
        ),
    ]
