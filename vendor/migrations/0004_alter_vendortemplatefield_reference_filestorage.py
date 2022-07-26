# Generated by Django 4.0.6 on 2022-07-26 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendor', '0003_alter_vendortemplate_template_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendortemplatefield',
            name='reference',
            field=models.CharField(choices=[('date', 'Date'), ('tax', 'Tax'), ('vate', 'Vat'), ('qty', 'Quantity'), ('unit_price', 'Unit Price'), ('amt', 'Amount')], max_length=100),
        ),
        migrations.CreateModel(
            name='FileStorage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='csvs')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
