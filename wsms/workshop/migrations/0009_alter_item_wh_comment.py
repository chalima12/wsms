# Generated by Django 4.2.7 on 2024-03-18 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0008_item_wh_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='wh_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
