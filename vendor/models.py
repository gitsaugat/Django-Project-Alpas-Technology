from turtle import onclick
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from users.models import UserRoles
import uuid
# Create your models here.
FIELDS_REFERENCE = [
    ('date', 'Date'),
    ('tax', 'Tax'),
    ('vate', 'Vat'),
    ('qty', 'Quantity'),
    ('unit_price', 'Unit Price'),
    ('amt', 'Amount'),
    ('paymentStat', 'Payment Status')
]


class VendorTemplate(models.Model):
    vendor = models.OneToOneField(User, on_delete=models.CASCADE)
    template_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.template_name

    def save(self, *args, **kwargs):
        if self.template_name == "" or self.template_name == None:
            self.template_name = f"{self.vendor.username} 's template"
        super(VendorTemplate, self).save(*args, **kwargs)


class VendorTemplateField(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    reference = models.CharField(choices=FIELDS_REFERENCE, max_length=100)
    template_field_key = models.CharField(max_length=100)
    referenced_template = models.ForeignKey(
        VendorTemplate, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Field for {self.referenced_template.template_name}"


class FileStorage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    file = models.FileField(upload_to='csvs')
    vendor = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.file.url


class VendorTemplateFieldData(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()
    file = models.ForeignKey(FileStorage, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.vendor.username + "data"


def create_vendor_template(sender, instance, created, **kwargs):
    if created:
        if instance.role.title.lower() == 'vendor':
            try:
                newvendortemplate = VendorTemplate.objects.create(
                    vendor=instance.user
                )
                newvendortemplate.save()
            except Exception as e:
                print(e)


post_save.connect(create_vendor_template, sender=UserRoles)
