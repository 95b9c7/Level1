# Generated by Django 5.1.5 on 2025-07-28 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waitapp', '0016_truckdriver_is_follow_up_truckdriver_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Active companies appear in driver selection'),
        ),
    ]
