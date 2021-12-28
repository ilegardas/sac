from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Permission

# Register your models here.

from personas.models import Departamento, Recurso, Proveedor, Requisicion, OrdenCompra, Compra, \
    Producto, Inventario, Bitacora, Usuario, Concepto, Venta, ConceptoVenta
admin.site.register(Permission)
#PERSONALIZACION DE LISTADO ADMIN DE USUARIOS
class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class UsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombres','username','email','apellidos','departamento_id__nombre']
    list_display = ('username', 'nombres', 'apellidos', 'email', 'telefono','departamento_id','is_active', 'is_staff' )
    resource_class = UsuarioResource

#PERSONALIZACION DE LISTADO ADMIN DE DEPARTAMENTOS
class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento

class DepartamentoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'descripcion')
    resource_class = DepartamentoResource

#PERSONALIZACION DE LISTADO ADMIN DE RECURSOS
class RecursoResource(resources.ModelResource):
    class Meta:
        model = Recurso

class RecursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'descripcion','fecha_creacion')
    resource_class = RecursoResource

#PERSONALIZACION DE LISTADO ADMIN DE PRODUCTOS
class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto

class ProductoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre','categoria']
    list_display = ('nombre', 'categoria','descripcion')
    resource_class = ProductoResource

#PERSONALIZACION DE LISTADO ADMIN DE PROVEEDORES
class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor

class ProveedorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre','descripcion','rfc','direccion']
    list_display = ('nombre', 'descripcion','telefono','email','rfc')
    resource_class = ProveedorResource

#PERSONALIZACION DE LISTADO ADMIN DE INVENTARIO
class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario

class InventarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['categoria','descripcion','unidad_medida','producto_id__nombre'] #producto_id__nombre para buscar por el nombre del producto no por id
    list_display = ('categoria', 'descripcion','producto_id','stock','stock_min','unidad_medida','fecha_creacion')
    resource_class = ProveedorResource

#PERSONALIZACION DE LISTADO ADMIN DE REQUISICIONES
class RequisicionResource(resources.ModelResource):
    class Meta:
        model = Requisicion

class RequisicionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['departamento_id__nombre','persona_id__nombre','descripcion','estatus'] #producto_id__nombre para buscar por el nombre del producto no por id
    list_display = ('id', 'departamento_id','persona_id','descripcion','estatus','fecha_creacion')
    resource_class = RequisicionResource

#PERSONALIZACION DE LISTADO ADMIN DE REQUISICIONES
class ConceptoResource(resources.ModelResource):
    class Meta:
        model = Concepto
class ConceptoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre','clave','fecha_creacion']
    list_display = ('id','nombre', 'clave','fecha_creacion')
    resource_class = ConceptoResource

#CLASS PARA EL ADMIN MANYTOMANY DE VENTAS Y CONCEPTOS
class ConceptoVentainLine(admin.TabularInline):
    model = ConceptoVenta
    extra = 1
    autocomplete_fields = ['concepto_id']

#PERSONALIZACION DE LISTADO ADMIN DE VENTAS
class VentaResource(resources.ModelResource):
    class Meta:
        model = Venta
class VentaAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    search_fields = ['concepto_id','monto','fecha_creacion']
    inlines = [ConceptoVentainLine, ]
    list_display = ('id', 'monto','fecha_creacion')
    resource_class = VentaResource



admin.site.register(Departamento,DepartamentoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Recurso,RecursoAdmin)
admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(Requisicion, RequisicionAdmin)
admin.site.register(OrdenCompra)
admin.site.register(Compra)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Inventario,InventarioAdmin)
admin.site.register(Bitacora)
admin.site.register(Concepto,ConceptoAdmin)
admin.site.register(Venta,VentaAdmin)
