# Generated by Django 3.0.2 on 2020-05-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_auto_20200428_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_billing_period',
            field=models.DateField(blank=True, null=True),
        ),
    ]
