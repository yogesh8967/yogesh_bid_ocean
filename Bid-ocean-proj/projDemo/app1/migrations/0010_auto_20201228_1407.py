# Generated by Django 3.1.4 on 2020-12-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20201228_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='Date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='Total_Sold',
            field=models.IntegerField(null=True),
        ),
    ]