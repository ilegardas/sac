# Generated by Django 3.2.8 on 2021-10-27 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0015_auto_20211025_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='estatus',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], default='pendiente', max_length=15, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='estatus',
            field=models.CharField(default='pendiente', max_length=15, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.FileField(blank=True, default=None, upload_to='perfil/', verbose_name='Imagen de perfil'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(default='', max_length=100, verbose_name='Clave'),
        ),
    ]