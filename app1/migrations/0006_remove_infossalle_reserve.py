# Generated by Django 4.1.5 on 2023-01-06 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_infossalle_date_de_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infossalle',
            name='reserve',
        ),
    ]
