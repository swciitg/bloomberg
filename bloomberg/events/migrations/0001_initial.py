

from django.db import migrations, models
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postedBy', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=128)),
                ('image', models.ImageField(default='images/profile_pic.png', upload_to='images/')),
                ('venue', models.CharField(max_length=128)),
                ('date', django_unixdatetimefield.fields.UnixDateTimeField()),
                ('organizingClub', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('isLive', models.BooleanField(default=False)),
                ('approvedBy', models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
