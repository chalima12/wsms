# Generated by Django 4.2.7 on 2023-11-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0006_alter_user_pass_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pass_word',
            field=models.CharField(max_length=50),
        ),
    ]
