from django.test import TestCase
from orders.models import Order


class OrderModelTest(TestCase):
    """ Тесты для модели Order """

    def test_create_order(self):
        """ Тестирует создание заказа и правильность расчета общей стоимости """

        order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Пицца', 'price': 300}, {'name': 'Салат', 'price': 150}],
            status='pending'
        )
        self.assertEqual(order.total_price, 450)

    def test_order_status_update(self):
        """ Тестирует обновление статуса заказа """

        order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Пицца', 'price': 300}],
            status='pending'
        )
        order.status = 'ready'
        order.save()
        self.assertEqual(order.status, 'ready')
