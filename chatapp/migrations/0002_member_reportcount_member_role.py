# Generated by Django 5.0.6 on 2024-05-16 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='ReportCount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='member',
            name='Role',
            field=models.CharField(default='member', max_length=10),
        ),
    ]
