# Generated by Django 4.2.7 on 2023-11-22 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0003_item_is_assigned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='is_assigned',
            new_name='assigned',
        ),
    ]
