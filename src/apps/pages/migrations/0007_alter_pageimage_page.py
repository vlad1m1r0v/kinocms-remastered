# Generated by Django 5.0.6 on 2024-07-25 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_remove_contact_created_at_contacts_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageimage',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pages.page'),
        ),
    ]
