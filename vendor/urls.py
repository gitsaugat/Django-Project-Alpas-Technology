from django import urls
from .views import VendorDashboard, VendorTemplateView, VendorTemplateSetup, VendorTemplateDelete, VendorTemplateEdit, CSV_handling_view, XLS_handling_view, AddConfirmation, Add_Confirm, Decline, VendorDataApi

urlpatterns = [
    urls.path('vendor/dashboard/', VendorDashboard.as_view(),
              name="vendors_dashboard"),
    urls.path('vendor/template/', VendorTemplateView.as_view(),
              name="vendor_template"),
    urls.path('vendor/template/setup/', VendorTemplateSetup.as_view(),
              name="vendor_template_setups"),
    urls.path('delete/vendor/field/<id>/', VendorTemplateDelete.as_view(),
              name="vendor_template_delete"),
    urls.path('edit/vendor/field/<id>/', VendorTemplateEdit.as_view(),
              name="vendor_template_edit"),
    urls.path('handle/csv/', CSV_handling_view.as_view(),
              name="handle_csv"),
    urls.path('handle/xls/', XLS_handling_view.as_view(),
              name="handle_xls"),
    urls.path('add/csv/data/<file_id>/<format_data>/',
              AddConfirmation.as_view(), name="data_add_confirmation_view"),
    urls.path('add/confirm/<file_id>/<format_data>/',
              Add_Confirm.as_view(), name="data_confirm_add_view"),
    urls.path('add/decline/<file_id>/',
              Decline.as_view(), name="data_decline_view"),
    urls.path('api/vendor_data/', VendorDataApi.as_view(),
              name="vendor_data_api")
]
