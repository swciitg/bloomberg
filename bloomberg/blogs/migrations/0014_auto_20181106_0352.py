# Generated by Django 2.1.2 on 2018-11-06 03:52

from django.db import migrations, models
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_merge_20181105_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='images/325505.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='createdAt',
            field=django_unixdatetimefield.fields.UnixDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='lastUpdated',
            field=django_unixdatetimefield.fields.UnixDateTimeField(auto_now=True),
        ),
    ]