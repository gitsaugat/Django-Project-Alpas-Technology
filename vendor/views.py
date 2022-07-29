
import pandas as pd
from curses.panel import update_panels
from django.conf import settings

from django.shortcuts import redirect, render
from django.views import View
from .models import VendorTemplate, VendorTemplateField, VendorTemplateFieldData
from .serializers import VendorInvoiceSerializer
from .forms import TemplateSetupForms
from django.contrib.messages import success, error, warning
from .utils import Csv_handling
from .models import FileStorage
import json
from AlpasProject.settings import BASE_DIR
import os
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class VendorDashboard(View):

    def get(self, request):
        return render(request, 'vendor/dashboard.html')


class VendorTemplateView(View):

    def get(self, request):
        template_fields = VendorTemplateField.objects.filter(
            referenced_template=VendorTemplate.objects.get(vendor=request.user))
        context = {
            'template_fields': template_fields,
            'title': 'Template'
        }
        return render(request, 'vendor/template.html', context)


class VendorTemplateSetup(View):

    def get(self, request):
        template_fields = VendorTemplateField.objects.filter(
            referenced_template=VendorTemplate.objects.get(vendor=request.user))

        context = {
            'form': TemplateSetupForms(),
            'title': 'Add Fields',
            'template_fields': template_fields
        }
        return render(request, 'vendor/templatesetup.html', context)

    def post(self, request):
        forms = TemplateSetupForms(request.POST)
        if forms.is_valid():
            try:
                vendor = VendorTemplateField.objects.get(
                    reference=forms.cleaned_data.get('reference'),
                    referenced_template=VendorTemplate.objects.get(
                        vendor=request.user)
                )
                error(request, 'Field Exists')
            except VendorTemplateField.DoesNotExist:
                try:
                    newfield = VendorTemplateField.objects.create(
                        reference=forms.cleaned_data.get('reference'),
                        template_field_key=forms.cleaned_data.get(
                            'template_field_key'),
                        referenced_template=VendorTemplate.objects.get(
                            vendor=request.user)
                    )
                    newfield.save()
                    success(request, 'Created')

                except Exception as e:
                    print(str(e))
                    error(request, 'Error occoured')
        return redirect('vendor_template_setups')


class VendorTemplateDelete(View):

    def get(self, request, id):
        context = {
            'title': 'Delete Fields'
        }
        try:
            field = VendorTemplateField.objects.get(id=id)
            field.delete()
            success(request, 'Field has ben successfully removed')
        except Exception as e:
            error(request, 'opps !')

        return redirect('vendor_template_setups')


class VendorTemplateEdit(View):

    def get(self, request, id):
        template_fields = VendorTemplateField.objects.filter(
            referenced_template=VendorTemplate.objects.get(vendor=request.user))

        context = {
            'form': TemplateSetupForms(instance=VendorTemplateField.objects.get(id=id)),
            'title': 'Add Fields',
            'template_fields': template_fields
        }
        return render(request, 'vendor/templatesetup.html', context)

    def post(self, request, id):
        forms = TemplateSetupForms(
            request.POST, instance=VendorTemplateField.objects.get(id=id))
        if forms.is_valid():

            forms.save()
            success(request, 'Updated')
            return redirect('vendor_template_setups')
        error(request, 'Couldnt Update')
        return redirect('vendor_template_setups')


class CSV_handling_view(View):

    def post(self, request):
        format = VendorTemplateField.objects.filter(
            referenced_template=VendorTemplate.objects.get(vendor=request.user))

        handling = Csv_handling()
        file = request.FILES['csv_file']
        data = handling.check_format(
            file, [field.template_field_key for field in format])
        try:
            file_storage = FileStorage.objects.create(
                file=file,
                vendor=request.user
            )
            file_storage.save()
            warning(
                request, f"seems like ther is a field missing in your template")
            return redirect(f'/add/csv/data/{file_storage.id}/{json.dumps(data)}')
        except Exception as e:
            print(e)
            error(request, "Seems like there is an issue"+str(e))
            return redirect('vendor_template')


class AddConfirmation(View):

    def get(self, request, file_id, format_data):
        handler = Csv_handling()
        ultimate_list = handler.get_ultimate_list(
            file_id, format_data)
        format_data = json.loads(format_data)

        context = {
            'title': 'Add Csv Data',
            'file_id': file_id,

            "format_data": format_data['matched'],
            'ultimate_list': ultimate_list,
            'json_format_data': json.dumps(format_data)
        }
        return render(request, 'vendor/add.html', context)


class Add_Confirm(View):

    def get(self, request, file_id, format_data):
        context = {
            'title': 'Add Csv Data'
        }
        handling = Csv_handling()
        print(format_data)
        ultimate_list = handling.get_ultimate_list(
            file_id, format_data)
        try:
            newdata = VendorTemplateFieldData.objects.create(
                vendor=request.user,
                data=json.dumps(ultimate_list),
                file=FileStorage.objects.get(id=file_id)
            )
            newdata.save()
            success(request, 'Yout data has been added')
            return redirect('vendor_template')
        except Exception as e:
            error(request, str(e))
            print(e)
        return render(request, 'vendor/confirm.html', context)


class Decline(View):

    def get(self, request, file_id):

        try:
            file = FileStorage.objects.get(id=file_id)
            file.file.delete()
            file.delete()
            success(request, 'Successfully Declined')
            return redirect('vendor_template_setups')
        except:
            error(request, 'Error while declininng')
        return redirect('vendor_template')


class XLS_handling_view(View):

    def post(self, request):
        pass


class VendorDataApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        data = VendorTemplateFieldData.objects.filter(
            vendor=request.user.id)
        serializer = VendorInvoiceSerializer(data, many=True)
        return Response(serializer.data)
