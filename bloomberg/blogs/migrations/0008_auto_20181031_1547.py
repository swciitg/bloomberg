# Generated by Django 2.1.2 on 2018-10-31 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20181031_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='blogID',
            field=models.CharField(max_length=11),
        ),
    ]
