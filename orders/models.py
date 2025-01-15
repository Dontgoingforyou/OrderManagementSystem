from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]

    table_number = models.PositiveIntegerField(verbose_name='номер стола')
    items = models.JSONField(verbose_name='список заказанных блюд с ценами')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='Общая сумма заказа')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args: tuple, **kwargs: dict) -> None:
        """ Сохраняет объект заказа, рассчитывая общую стоимость на основе списка блюд """

        self.total_price = sum(item['price'] for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """ Возвращает строковое представление объекта заказа """

        return f'Заказ {self.id}, стол {self.table_number}'
