# Generated by Django 3.2.8 on 2021-11-03 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0016_auto_20211026_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bitacora',
            name='persona_id',
        ),
        migrations.AddField(
            model_name='bitacora',
            name='usuario',
            field=models.CharField(default=None, max_length=50, verbose_name='Nombre'),
        ),
    ]