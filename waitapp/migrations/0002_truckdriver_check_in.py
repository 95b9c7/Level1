# Generated by Django 3.2.21 on 2023-11-03 15:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('waitapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='truckdriver',
            name='check_in',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
