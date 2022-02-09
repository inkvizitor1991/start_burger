from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import F, Sum
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                .filter(availability=True)
                .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class CostQuerySet(models.QuerySet):
    def count_price(self):
        total_price = self.annotate(
            total_price=Sum(F('order_product__quantity') * F('order_product__fixed_price')))
        return total_price


class Order(models.Model):
    ORDER_PROCESSED = 'processed'
    ORDER_UNPROCESSED = 'unprocessed'
    STATUS = [
        (ORDER_PROCESSED, 'Обработанный заказ'),
        (ORDER_UNPROCESSED, 'Не обработанный заказ'),
    ]
    CASH = 'cash'
    CASHLESS = 'cashless'
    NOT_SELECTED = 'not_selected'
    PAYMENT_METHOD = [
        (CASH, 'Наличностью'),
        (CASHLESS, 'Электронно'),
        (NOT_SELECTED, 'Не выбранно')
    ]
    firstname = models.CharField(
        'Имя',
        max_length=35,
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=35,
    )
    phonenumber = PhoneNumberField(
        'Номер телефона',
        db_index=True
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=100,
    )
    status_order = models.CharField(
        'Статус заказа',
        choices=STATUS,
        default=ORDER_UNPROCESSED,
        max_length=30,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        null=True,
        blank=True,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='ресторан'
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PAYMENT_METHOD,
        default=NOT_SELECTED,
        max_length=30,
        db_index=True
    )
    comment = models.TextField(
        'Комментарий',
        max_length=200,
    )
    registered_at = models.DateTimeField(
        'Дата оформления заказа',
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        'Дата звонка',
        db_index=True,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        'Дата доставки',
        db_index=True,
        null=True,
        blank=True,
    )
    objects = CostQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname}, {self.address}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_products',
        verbose_name='заказчик',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='order_products',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)]
    )
    fixed_price = models.DecimalField(
        'фиксированная цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = 'заказанный товар'
        verbose_name_plural = 'заказанные товары'

    def __str__(self):
        return f"{self.product}"


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"
