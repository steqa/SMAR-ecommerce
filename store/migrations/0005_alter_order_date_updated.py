# Generated by Django 4.1.2 on 2022-10-21 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]