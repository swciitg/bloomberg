# Generated by Django 2.1.2 on 2019-01-13 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20181230_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='totalVotes',
            field=models.IntegerField(default=0),
        ),
    ]
