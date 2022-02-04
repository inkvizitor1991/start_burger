# Generated by Django 3.2 on 2022-01-29 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_restaurantmenuitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
    ]
