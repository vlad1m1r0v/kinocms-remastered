# Generated by Django 5.0.6 on 2024-06-28 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
