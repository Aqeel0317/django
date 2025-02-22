# Generated by Django 5.1.2 on 2024-11-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_saleannouncement'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleannouncement',
            name='background_color',
            field=models.CharField(default='#ff5722', help_text='Background color of the banner (in hex, e.g., #ff5722).', max_length=7),
        ),
        migrations.AddField(
            model_name='saleannouncement',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text="Discount percentage or amount (e.g., '20%' or '$40').", max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='saleannouncement',
            name='image',
            field=models.ImageField(blank=True, help_text='Image for the sale banner.', null=True, upload_to='sale_images/'),
        ),
        migrations.AlterField(
            model_name='saleannouncement',
            name='message',
            field=models.CharField(help_text="Short message for the sale (e.g., '20% OFF').", max_length=255),
        ),
    ]
