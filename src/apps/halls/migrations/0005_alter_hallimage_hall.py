# Generated by Django 5.0.6 on 2024-07-30 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0004_rename_cinema_hallimage_hall_seat_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallimage',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='halls.hall'),
        ),
    ]
