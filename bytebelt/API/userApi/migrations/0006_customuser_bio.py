# Generated by Django 5.0.6 on 2024-06-21 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApi', '0005_customuser_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
