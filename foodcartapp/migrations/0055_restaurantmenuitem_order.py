# Generated by Django 3.2 on 2022-01-27 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantmenuitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.order', verbose_name='заказ'),
        ),
    ]
