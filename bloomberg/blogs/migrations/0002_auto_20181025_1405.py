# Generated by Django 2.1.2 on 2018-10-25 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
