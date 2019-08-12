
from django.forms import ModelForm, forms
from web import models

class PaymentForm(ModelForm):
    class Meta:
        model = models.Payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placehold'] = field.label
        self.fields['customer'].empty_label = "请选择客户"

