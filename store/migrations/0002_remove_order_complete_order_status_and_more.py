# Generated by Django 4.1.1 on 2022-10-17 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('1', 'Ожидает отправки'), ('2', 'Отправлен'), ('3', 'Выполнен')], default='Ожидает отправки', max_length=16),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shippingaddress', to='store.order'),
        ),
    ]
