# Generated by Django 5.0 on 2024-01-22 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_business_bus_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='bus_img',
            field=models.ImageField(default='storefront.svg', null=True, upload_to=''),
        ),
    ]
