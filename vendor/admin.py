from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(VendorTemplate)
admin.site.register(VendorTemplateField)
admin.site.register(VendorTemplateFieldData)
admin.site.register(FileStorage)
