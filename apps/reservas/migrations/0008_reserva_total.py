# Generated by Django 5.2.2 on 2025-06-12 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0007_alter_reserva_menu_delete_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
