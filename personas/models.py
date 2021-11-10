from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.hashers import make_password

# Create your models here.

class UsuarioManager(BaseUserManager):
    def _create_user(self,username, email, nombres, apellidos, password, is_staff, is_superuser,**extra_fields):
        usuario = self.model(
            username=username,
            email=email,
            nombres=nombres,
            apellidos=apellidos,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        usuario.password = make_password(password, salt=None, hasher='default')
        return user
    def create_user(self, username, email, nombres, apellidos, password = None,**extra_fields):
        return self._create_user(username, email, nombres, apellidos, password, False, False, **extra_fields)
    def create_superuser(self, username, email, nombres, apellidos, password = None,**extra_fields):
        return self._create_user(username,email,nombres,apellidos,True,True,**extra_fields)




    def create_superuser(self,username,email,nombres,apellidos,password):
        usuario = self.create_user(
            email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password
        )
        usuario.usuario_administrador = True

        return usuario


class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre Departamento', max_length=45, null=True, blank=False)
    descripcion = models.TextField('Descripcion Departamento', max_length=250, null=False, blank=False)
    #fecha_creado = models.DateField('Fecha de Creacion:', auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Usuario(AbstractBaseUser,PermissionsMixin):
    username = models.CharField('Nombre de Usuario', unique=True, max_length=40, default='pendiente')
    password = models.CharField('Clave',default='', max_length=100)
    email = models.EmailField('Correo Electronico ', max_length=100, unique=True, default='1@2.com')
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True )
    departamento_id = models.ForeignKey('Departamento', on_delete=models.PROTECT, null=True, blank=True )
    imagen = models.FileField('Imagen de perfil', upload_to='perfil/', default=None, blank=True)
    telefono = models.CharField('Telefono', max_length=15)
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Administrador',default=False)
    objects= UsuarioManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres','apellidos']

    def UsuarioDepartamento(self):
        return self.departamento_id

    def ObtenerID(self):
        return self.id

    def __str__(self):
        return f' {self.nombres}, {self.apellidos} '

class Recurso(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=25, null=False, blank=False)
    descripcion = models.TextField('Descripcion', max_length=250)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=True, auto_created=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=25, null=False, blank=False)
    descripcion = models.CharField('Descripcion', max_length=250)
    telefono = models.CharField('Telefono', max_length=25)
    email = models.CharField('Email', max_length=40)
    rubro = models.CharField('Rubro', max_length=25)
    direccion = models.TextField('Direccion', max_length=355, null=False, blank=False)
    rfc = models.CharField('RFC',max_length=30)
    contacto = models.CharField('Contacto', max_length=50)
    fecha_creacion = models.DateField( 'Fecha de Creacion', auto_now=True, auto_created=True )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=25, null=False, blank=False)
    categoria = models.CharField('Categoria',  max_length=25, null=False, blank=False, default='' )
    descripcion = models.TextField('Descripcion', max_length=250 )
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=True, auto_created=True )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField('Categoria', max_length=25)
    unidad_medida = models.CharField('Unidad de Medida', max_length=15)
    descripcion = models.TextField('Descripcion', max_length=250)
    stock = models.CharField('Stock', max_length=15)
    stock_min = models.CharField('Stock Minimo', max_length=15)
    producto_id = models.ForeignKey('Producto', on_delete=models.PROTECT)
    fecha_creacion = models.DateField( 'Fecha de Creacion', auto_now=True, auto_created=True )

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['categoria']

    def __str__(self):
        return self.categoria

class Requisicion(models.Model):
    id = models.AutoField(primary_key=True)
    departamento_id = models.ForeignKey('Departamento', on_delete=models.PROTECT )
    persona_id = models.ForeignKey('Usuario', on_delete=models.PROTECT , default= None)
    concepto = models.CharField('Concepto', max_length=50)
    producto_id = models.ForeignKey('Producto',default=None, on_delete=models.PROTECT)
    descripcion = models.TextField('Descripcion', max_length=250, blank=True)
    estatus = models.CharField('Estatus', max_length=15, default='pendiente' )
    fecha_estatus = models.DateField('Fecha de Estatus ')
    fecha_creacion = models.DateField( 'Fecha de Creacion', auto_created=True )

    class Meta:
        verbose_name = 'Requisicion'
        verbose_name_plural = 'Requisiciones'
        ordering = ['id']

    def __str__(self):
        return self.id

class OrdenCompra(models.Model):
    id = models.AutoField(primary_key=True)
    requerimiento_id = models.OneToOneField('Requisicion', on_delete=models.PROTECT, default=None)
    aprobador_id = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    recursos_id = models.ForeignKey('Recurso', on_delete=models.PROTECT)
    proveedor_id = models.ForeignKey('Proveedor', on_delete=models.PROTECT)
    producto_id = models.ForeignKey( 'Producto', on_delete=models.PROTECT )
    descripcion = models.TextField( 'Descripcion', max_length=250, null=True )
    estatus = models.CharField('Estatus',  max_length=15, default='pendiente')
    fecha_estatus = models.DateField( 'Fecha de Estatus ' )
    fecha_creacion = models.DateField( 'Fecha de Creacion', auto_created=True )
    impresa = models.CharField('Veces Impresa', max_length=5, default=0)
    cantidad_prod = models.CharField( 'Cantidad', default=1, max_length=20 )
    precio_unitario = models.CharField( 'Precio Unitario', max_length=60, default=0 )
    precio_total = models.CharField( 'Precio Total', max_length=60, default=0 )

    class Meta:
        verbose_name = 'OrdenCompra'
        verbose_name_plural = 'OrdenesCompras'
        ordering = ['id']

    def __str__(self):
        return str(self.id)
compra_estatus = [
    ('pendiente','Pendiente'),
    ('pagado','Pagado'),


]
class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    ordenCompra_id = models.OneToOneField('OrdenCompra', on_delete=models.PROTECT, default=None)
    aprobador_id = models.ForeignKey('Usuario', on_delete=models.PROTECT)
    descripcion = models.TextField('Descripcion', max_length=300,default=None)
    pdf = models.FileField('PDF', upload_to='pdf/', blank=True, null=True)
    xml = models.FileField('XML', upload_to='xml/', blank=True, null=True)
    Total = models.CharField('Total',max_length=20, default=None)
    estatus = models.CharField(
        'Estatus',  max_length=15,
        default='pendiente',
        choices=compra_estatus
    )
    fecha_estatus = models.DateField( 'Fecha de Estatus ' )
    fecha_creacion = models.DateField( 'Fecha de Creacion', auto_created=True )


    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

    def __str__(self):
        return self.id

class Bitacora(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField('Nombre', max_length=60, default=None)
    tipo_documento = models.CharField('Tipo Documento', max_length=70, default=None)
    folio = models.CharField('Id', max_length=60)
    estatus = models.CharField('Estatus', max_length=60)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=True, auto_created=True)