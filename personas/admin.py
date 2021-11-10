from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Permission

# Register your models here.

from personas.models import Departamento, Recurso, Proveedor, Requisicion, OrdenCompra, Compra, \
    Producto, Inventario, Bitacora, Usuario
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
    search_fields = ['nombre','descripcion','rubro','contacto','rfc','direccion']
    list_display = ('nombre', 'descripcion','telefono','email','rfc','rubro')
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
    search_fields = ['departamento_id__nombre','persona_id__nombre','concepto','descripcion','estatus'] #producto_id__nombre para buscar por el nombre del producto no por id
    list_display = ('id', 'departamento_id','persona_id','concepto','descripcion','estatus','fecha_creacion')
    resource_class = RequisicionResource

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
