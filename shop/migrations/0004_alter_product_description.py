# Generated by Django 5.1.2 on 2024-11-06 05:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_specifications_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
