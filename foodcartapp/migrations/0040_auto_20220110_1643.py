# Generated by Django 3.2 on 2022-01-10 16:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_auto_20220110_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=10, verbose_name='Имя')),
                ('lastname', models.CharField(max_length=15, verbose_name='Фамилия')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=30, verbose_name='Адрес доставки')),
            ],
            options={
                'verbose_name': 'покупатель',
                'verbose_name_plural': 'покупатели',
            },
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='product',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='foodcartapp.product', verbose_name='Продукт'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=2000, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.registration', verbose_name='заказчик'),
        ),
    ]