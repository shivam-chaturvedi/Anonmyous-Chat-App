# Generated by Django 5.0.6 on 2024-05-18 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0004_member_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='Status',
            new_name='isOnline',
        ),
    ]
