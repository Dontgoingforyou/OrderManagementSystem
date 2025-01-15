from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Order
from .forms import OrderForm, OrderFilterForm
from django.db.models import Sum
from typing import Dict, Any


class OrderListView(ListView):
    """ Представление для отображения списка заказов с фильтрацией """

    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    form_class = OrderFilterForm

    def get_queryset(self):
        """ Возвращает отфильтрованный список заказов, если применены фильтры """

        queryset = Order.objects.all()

        table_number = self.request.GET.get('table_number')
        if table_number:
            queryset = queryset.filter(table_number=table_number)

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """ Добавляет форму фильтра в контекст, чтобы отображать ее на странице """

        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class(self.request.GET)
        return context


class OrderCreateView(CreateView):
    """ Представление для создания нового заказа """

    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """ Добавляет форму фильтра в контекст, чтобы отображать ее на странице """

        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class OrderUpdateView(UpdateView):
    """ Представление для обновления существующего заказа """

    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def form_valid(self, form: OrderForm) -> Any:
        """ Обрабатывает сохранение формы при успешной валидации """

        form.instance.items = form.cleaned_data['items_input']
        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    """ Представление для удаления заказа """

    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order_list')


class RevenueView(TemplateView):
    """ Представление для отображения общей выручки """

    template_name = 'orders/revenue.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """ Добавляет общую сумму выручки в контекст """

        context = super().get_context_data(**kwargs)
        context['revenue'] = Order.objects.filter(status='paid').aggregate(total=Sum("total_price"))["total"] or 0
        return context
