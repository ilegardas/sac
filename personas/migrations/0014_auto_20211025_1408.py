# Generated by Django 3.2.8 on 2021-10-25 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0013_auto_20211022_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='uploads/compras/', verbose_name='PDF'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='xml',
            field=models.FileField(blank=True, null=True, upload_to='uploads/compras/', verbose_name='XML'),
        ),
    ]
