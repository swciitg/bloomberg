# Generated by Django 2.1.3 on 2018-11-10 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0020_auto_20181110_1218'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserDetails',
            new_name='UserDetail',
        ),
    ]
