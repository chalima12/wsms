# Generated by Django 4.2.6 on 2023-10-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_remove_component_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
