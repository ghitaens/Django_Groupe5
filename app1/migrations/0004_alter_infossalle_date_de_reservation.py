# Generated by Django 4.1.5 on 2023-01-06 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_infossalle_date_de_reservation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infossalle',
            name='date_de_reservation',
            field=models.DateField(default='0000-00-00'),
        ),
    ]
