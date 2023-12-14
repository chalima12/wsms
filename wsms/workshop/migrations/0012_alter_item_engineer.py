# Generated by Django 4.2.7 on 2023-12-12 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0011_alter_item_is_damage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='engineer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engineers', to=settings.AUTH_USER_MODEL),
        ),
    ]