# Generated by Django 3.1.4 on 2020-12-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dish_Name', models.CharField(max_length=200, null=True)),
                ('Dish_Discription', models.CharField(max_length=200, null=True)),
                ('Dish_Type', models.CharField(choices=[('Indian', 'Indian'), ('Chinesse', 'Chinesse'), ('Western', 'Western')], max_length=200, null=True)),
                ('Price', models.FloatField(max_length=200, null=True)),
                ('Offer', models.IntegerField(max_length=200, null=True)),
                ('Dish_File_Path', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
