# Generated by Django 3.0.2 on 2020-04-21 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20200421_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='description',
            field=models.CharField(default='description', max_length=100),
        ),
    ]
