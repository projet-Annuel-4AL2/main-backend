# Generated by Django 5.0.6 on 2024-06-24 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupe', '0008_rename_group_pic_groupepublication_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupepublication',
            old_name='image',
            new_name='group_pic',
        ),
    ]
