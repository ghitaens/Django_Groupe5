# Generated by Django 4.1.5 on 2023-01-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infossalle',
            name='nombre_invite',
            field=models.IntegerField(),
        ),
    ]
