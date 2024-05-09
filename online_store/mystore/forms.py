from django import forms
from django.core.exceptions import ValidationError

from mystore.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 5:
            raise ValidationError({
                "description": "Описание не может быть менее 5 символов."
            })

        name = cleaned_data.get("name")
        if description == name:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

    def get_name(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        return name


