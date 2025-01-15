from django import forms
from orders.models import Order
from typing import List, Dict, Any


class OrderForm(forms.ModelForm):
    items_input = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Список заказанных блюд",
        help_text="Введите в формате: Пицца 100, Суп 200",
    )

    class Meta:
        model = Order
        fields = ['table_number', 'status']
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """ Инициализация формы. Если экземпляр модели уже существует,
        конвертируем список заказанных блюд в строку для поля items_input """

        super().__init__(*args, **kwargs)
        if self.instance and self.instance.items:
            items = self.instance.items
            items_str = ", ".join([f"{item['name']} {item['price']}" for item in items])
            self.fields['items_input'].initial = items_str

    def clean_items_input(self) -> List[Dict[str, Any]]:
        """ Конвертирует пользовательский ввод в формат JSON """

        raw_items = self.cleaned_data['items_input']
        items = []

        try:
            for item in raw_items.split(','):
                parts = item.strip().rsplit(maxsplit=1)

                if len(parts) != 2:
                    raise ValueError("Каждое блюдо должно быть в формате: название цена (через пробел)")
                name, price = parts
                items.append({"name": name, "price": float(price)})
        except ValueError:
            raise forms.ValidationError(
                "Введите данные в формате: Блюдо цена, Блюдо цена (например: Пицца 100, Суп 200)"
            )
        return items

    def save(self, commit: bool = True) -> Order:
        """ Перенос данных из items_input в поле items """

        self.instance.items = self.cleaned_data['items_input']
        return super().save(commit)


class OrderFilterForm(forms.Form):
    table_number = forms.IntegerField(required=False, label='Номер стола')
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES, required=False, label='Статус заказа')
