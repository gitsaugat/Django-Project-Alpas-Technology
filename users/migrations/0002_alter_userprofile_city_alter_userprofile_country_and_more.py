# Generated by Django 4.0.6 on 2022-07-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile_no',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='telephone_no',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zip_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
