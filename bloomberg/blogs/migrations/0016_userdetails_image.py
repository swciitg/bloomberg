# Generated by Django 2.1.3 on 2018-11-06 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_merge_20181106_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='image',
            field=models.ImageField(default='images/325505.jpg', upload_to='images/'),
        ),
    ]
