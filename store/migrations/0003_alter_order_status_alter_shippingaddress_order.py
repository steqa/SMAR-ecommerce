# Generated by Django 4.1.2 on 2022-10-21 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_order_complete_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(False, 'Не оформлен'), ('1', 'Ожидает отправки'), ('2', 'Отправлен'), ('3', 'Выполнен')], default=False, max_length=16),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order'),
        ),
    ]
