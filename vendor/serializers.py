from rest_framework.serializers import ModelSerializer
from .models import VendorTemplateFieldData


class VendorInvoiceSerializer(ModelSerializer):

    class Meta:
        model = VendorTemplateFieldData
        fields = "__all__"
