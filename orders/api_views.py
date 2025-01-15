from rest_framework import generics
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """ API view для получения списка всех заказов и создания нового заказа """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ API view для получения, обновления или удаления заказа по его ID """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
