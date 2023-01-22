# Generated by Django 4.1.5 on 2023-01-21 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('fecha_creacion', models.DateField(auto_created=True, verbose_name='Fecha de Creacion')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('edad', models.CharField(max_length=3, verbose_name='Edad')),
                ('sexo', models.CharField(max_length=30, verbose_name='Sexo')),
                ('estado_civil', models.CharField(max_length=40, verbose_name='Estado Civil')),
                ('domicilio', models.CharField(max_length=300, verbose_name='Domicilio')),
                ('fecha_remision', models.DateField(verbose_name='Fecha Remision')),
                ('hora', models.TimeField(verbose_name='Hora')),
                ('motivo', models.TextField(default=None, max_length=500, verbose_name='Descripcion')),
                ('evidencia', models.FileField(blank=True, null=True, upload_to='jpg/', verbose_name='JPG')),
                ('pertenencias', models.CharField(max_length=300, verbose_name='Pertenencias')),
                ('agentes', models.CharField(max_length=300, verbose_name='Agentes que detienen')),
                ('lugar', models.CharField(max_length=300, verbose_name='Lugar')),
                ('formato_pago', models.CharField(max_length=300, verbose_name='Formato de Pago')),
                ('salida', models.DateTimeField(verbose_name='Fecha de salida')),
                ('autorizacion_salida', models.CharField(max_length=100, verbose_name='Autorizacion de Salida')),
                ('visible', models.CharField(default='si', max_length=100, verbose_name='visible')),
            ],
            options={
                'verbose_name': 'Incidencia',
                'verbose_name_plural': 'Incidencias',
                'ordering': ['id'],
            },
        ),
    ]
