# Generated by Django 5.0 on 2024-01-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_customer_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_num',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
