# Generated by Django 3.0.2 on 2020-04-28 14:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_delete_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='initiated_on',
            field=models.DateField(auto_now_add=True, default=datetime.date(2020, 4, 28)),
            preserve_default=False,
        ),
    ]
