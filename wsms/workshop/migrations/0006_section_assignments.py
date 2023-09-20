# Generated by Django 4.2.5 on 2023-09-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0005_remove_assignments_engineer_remove_assignments_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('section_id', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.section')),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.users')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.item')),
            ],
        ),
    ]
