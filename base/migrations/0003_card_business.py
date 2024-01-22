# Generated by Django 5.0 on 2024-01-20 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gift_cards', to='base.business'),
        ),
    ]
