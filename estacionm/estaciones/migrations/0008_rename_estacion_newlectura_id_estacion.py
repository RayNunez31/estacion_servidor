# Generated by Django 4.2.13 on 2024-07-15 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estaciones', '0007_alter_estac_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newlectura',
            old_name='estacion',
            new_name='id_estacion',
        ),
    ]
