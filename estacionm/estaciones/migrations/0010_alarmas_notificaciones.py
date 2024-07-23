# Generated by Django 4.2.13 on 2024-07-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estaciones', '0009_alter_newlectura_options_alter_sensor_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarmas',
            fields=[
                ('id_alarma', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('temperatura', models.FloatField(blank=True, null=True)),
                ('humedad', models.FloatField(blank=True, null=True)),
                ('presionatmosferica', models.FloatField(blank=True, null=True)),
                ('velocidad_del_viento', models.FloatField(blank=True, null=True)),
                ('direccion_del_viento', models.FloatField(blank=True, null=True)),
                ('pluvialidad', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'alarmas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'notificaciones',
                'managed': False,
            },
        ),
    ]
