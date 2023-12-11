# Generated by Django 4.2.7 on 2023-11-27 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0005_alter_item_assigned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='delivered_by',
        ),
        migrations.AddField(
            model_name='item',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]