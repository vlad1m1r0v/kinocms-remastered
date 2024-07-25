# Generated by Django 5.0.6 on 2024-07-25 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0002_hall_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hall',
            name='capacity',
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.SmallIntegerField()),
                ('column', models.SmallIntegerField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='halls.hall')),
            ],
        ),
    ]
