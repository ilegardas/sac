# Generated by Django 3.2.8 on 2021-10-25 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0014_auto_20211025_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='estatus',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado'), ('terminado', 'Terminado')], default='pendiente', max_length=15, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdf/', verbose_name='PDF'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='xml',
            field=models.FileField(blank=True, null=True, upload_to='xml/', verbose_name='XML'),
        ),
    ]