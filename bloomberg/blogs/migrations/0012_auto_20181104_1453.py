# Generated by Django 2.1.2 on 2018-11-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_auto_20181102_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-createdAt']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='approvedBy',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
