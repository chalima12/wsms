# Generated by Django 4.2.5 on 2023-09-19 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0006_section_assignments'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='remark',
            field=models.TextField(null=True),
        ),
    ]
