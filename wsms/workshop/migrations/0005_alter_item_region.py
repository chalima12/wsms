# Generated by Django 4.2.7 on 2024-03-12 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_alter_item_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='workshop.district'),
            preserve_default=False,
        ),
    ]
