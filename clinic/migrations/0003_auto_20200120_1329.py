# Generated by Django 2.2.9 on 2020-01-20 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_auto_20200120_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
