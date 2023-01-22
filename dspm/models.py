from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.hashers import make_password

# Create your models here.
from django.forms import model_to_dict
# Create your models here.
class Incidencia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=100)
    edad = models.CharField('Edad',max_length=3,default=None, null=True, blank=True)
    sexo = models.CharField('Sexo',max_length=30,default=None, null=True, blank=True)
    estado_civil = models.CharField('Estado Civil', max_length=40,default=None, null=True, blank=True)
    domicilio = models.CharField('Domicilio', max_length=300,default=None, null=True, blank=True)
    fecha_remision = models.DateField('Fecha Remision')
    hora = models.TimeField('Hora')
    motivo = models.TextField('Descripcion', max_length=500,default=None)
    evidencia = models.FileField('JPG', upload_to='jpg/', blank=True, null=True,)
    pertenencias = models.CharField('Pertenencias',max_length=300,default=None, null=True, blank=True)
    agentes = models.CharField('Agentes que detienen',max_length=300,default=None, null=True, blank=True)
    lugar = models.CharField('Lugar',max_length=300,default=None, null=True, blank=True)
    formato_pago = models.CharField('Formato de Pago',max_length=300,default=None, null=True, blank=True)
    salida = models.DateTimeField('Fecha de salida',default=None, null=True, blank=True)
    autorizacion_salida = models.CharField('Autorizacion de Salida',max_length=100,default=None, null=True, blank=True)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_created=True)
    creado_por = models.ForeignKey('personas.Usuario', on_delete=models.PROTECT, default=None)
    visible = models.CharField('visible', max_length=100, null=False, blank=False, default='si')

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        ordering = ['id']
