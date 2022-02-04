# Generated by Django 3.2 on 2022-02-04 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0058_auto_20220204_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.order', verbose_name='заказчик'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
