# Generated by Django 5.0.6 on 2024-07-15 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estaciones', '0002_newlectura'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('modelo', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'Sensor',
                'managed': False,
            },
        ),
    ]
