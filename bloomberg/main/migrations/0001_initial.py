# Generated by Django 2.1.3 on 2018-12-26 08:20

from django.db import migrations, models
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=50)),
                ('emailID', models.EmailField(max_length=50)),
                ('logInTime', django_unixdatetimefield.fields.UnixDateTimeField(blank=True, null=True)),
                ('logOutTime', django_unixdatetimefield.fields.UnixDateTimeField(null=True)),
                ('isExpired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=50)),
                ('emailID', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('image', models.ImageField(default='images/profile_pic.png', upload_to='images/')),
                ('mobile', models.IntegerField()),
                ('totalBlogsWritten', models.IntegerField(default=0)),
                ('isBlocked', models.BooleanField(default=False)),
                ('isAdmin', models.BooleanField(default=False)),
                ('isModerator', models.BooleanField(default=False)),
            ],
        ),
    ]
