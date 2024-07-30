from django import forms

from resources.sales.models import Invoice


class InvoiceForm(forms.ModelForm):
    pdf_file = forms.FileField(required=False)

    class Meta:
        model = Invoice
        fields = '__all__'
