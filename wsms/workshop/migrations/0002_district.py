# Generated by Django 4.2.7 on 2024-03-12 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
            ],
        ),
    ]
