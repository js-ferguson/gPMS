# Generated by Django 3.0.2 on 2020-04-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200225_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sub_type',
            field=models.CharField(default=0, max_length=20),
        ),
    ]
