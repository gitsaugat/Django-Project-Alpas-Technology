from django import forms
from .models import VendorTemplateField


class TemplateSetupForms(forms.ModelForm):
    class Meta:
        model = VendorTemplateField
        fields = '__all__'
        exclude = ['id', 'referenced_template']
        labels = {
            'reference': 'Field Type',
            'template_field_key': 'Custom Name'
        }
