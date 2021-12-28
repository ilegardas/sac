"""sac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from personas.views import Home, SinPermisos, ListarBitacora, CrearVenta, ListarVentas, \
    EditarVenta, EliminarVenta, CrearConcepto, ListarConceptos, EditarConcepto, \
    EliminarConcepto, CrearVehiculo, ListarVehiculo, EditarVehiculo, EliminarVehiculo, \
    CrearTiposVehiculo, ListarTiposVehiculos, EditarTiposVehiculo, EliminarTiposVehiculo, \
    ReporteVehiculos  # , logout_user, login_user
from personas.views import CrearDepartamento, ListarDepartamentos, EditarDepartamento, EliminarDepartamento, CrearRecurso, ListarRecursos, EditarRecurso, EliminarRecurso, CrearProducto, EditarProducto, ListarProductos, EliminarProducto
from personas.views import CrearProveedor, ListarProveedores,EditarProveedor,EliminarProveedor, CrearInventario, ListarInventarios, EditarInventario, EliminarInventario, CrearRequisicion, ListarRequisiciones, EditarRequisicion, EliminarRequisicion
from personas.views import CrearOrden, ListarOrdenes, EditarOrden, EliminarOrden, CancelarRequisicion, CancelarOrden, ImprimirOrden, ContadorImpresiones, CrearCompra, EditarCompra, CancelarCompra, ListarCompras, EliminarCompra, TerminarCompra, CrearUsuario, EditarUsuario, ListarUsuarios, EliminarUsuario, ReporteRequerimientos, ReporteOrdenes, ReporteCompras, cambiar_logo, ImprimirRequisicion, TerminarRequisicion
from personas import views
from django.contrib.auth.decorators import login_required, permission_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='inicio'), #path recibe 3 parametros texto de barra de direcciones, la funcion a ehecutar y un nombre de url

    #CAMBIAR LOGO DE FORMATOS
    path('cambiar-logotipo/',permission_required('personas.delete_usuario', login_url='')(cambiar_logo), name='cambiar-logo' ),

    #INICIO DE SESION
    path('accounts/', include('django.contrib.auth.urls')),
    path('salir', views.salir, name='salir'),
    # SEGMENTO PARA DEPARTAMENTOS
    # ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('usuarios/crear_usuario/',permission_required('personas.add_usuario', login_url='')(CrearUsuario), name='crear_usuario' ),
    path('usuarios/listar_usuarios/',permission_required('personas.view_usuario', login_url='')(ListarUsuarios), name='listar_usuarios' ),
    path('usuarios/editar_usuario/<int:id>',permission_required('personas.change_usuario', login_url='')(EditarUsuario), name='editar_usuario' ),
    path('usuarios/eliminar_usuario/<int:id>',permission_required('personas.delete_usuario', login_url='')(EliminarUsuario), name='eliminar_usuario' ),


    #SEGMENTO PARA DEPARTAMENTOS
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('departamentos/crear_departamento/',permission_required('personas.add_departamento', login_url='')(CrearDepartamento), name='crear_departamento'),
    path('departamentos/listar_departamentos/',permission_required('personas.view_departamento', login_url='')(ListarDepartamentos), name='listar_departamentos'),
    path('departamentos/editar_departamentos/<int:id>',permission_required('personas.change_departamento', login_url='')(EditarDepartamento), name='editar_departamento'),
    path('departamentos/eliminar_departamentos/<int:id>',permission_required('personas.delete_departamento', login_url='')(EliminarDepartamento), name='eliminar_departamento'),

#SEGMENTO PARA DEPARTAMENTOS
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('recursos/crear_recurso/',permission_required('personas.add_recurso', login_url='')(CrearRecurso), name='crear_recurso'),
    path('recursos/listar_recursos/',permission_required('personas.view_recurso', login_url='')(ListarRecursos), name='listar_recursos'),
    path('recursos/editar_recursos/<int:id>',permission_required('personas.change_recurso', login_url='')(EditarRecurso), name='editar_recurso'),
    path('recursos/eliminar_recursos/<int:id>',permission_required('personas.delete_recurso', login_url='')(EliminarRecurso), name='eliminar_recurso'),


#SEGMENTO PARA PRODUCTOS
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('productos/crear_producto/',permission_required('personas.add_producto', login_url='')(CrearProducto), name='crear_producto'),
    path('productos/listar_productos/',permission_required('personas.view_producto', login_url='')(ListarProductos), name='listar_productos'),
    path('productos/editar_productos/<int:id>',permission_required('personas.change_producto', login_url='')(EditarProducto), name='editar_producto'),
    path('productos/eliminar_productos/<int:id>',permission_required('personas.delete_producto', login_url='')(EliminarProducto), name='eliminar_producto'),


#SEGMENTO PARA PROVEEDORES
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('proveedores/crear_proveedor/',permission_required('personas.add_proveedor', login_url='')(CrearProveedor), name='crear_proveedor'),
    path('proveedores/listar_proveedores/',permission_required('personas.view_proveedor', login_url='')(ListarProveedores), name='listar_proveedores'),
    path('proveedores/editar_proveedores/<int:id>',permission_required('personas.change_proveedor', login_url='')(EditarProveedor), name='editar_proveedor'),
    path('proveedores/eliminar_proveedores/<int:id>',permission_required('personas.delete_proveedor', login_url='')(EliminarProveedor), name='eliminar_proveedor'),


#SEGMENTO PARA INVENTARIOS
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('inventarios/crear_inventario/',permission_required('personas.add_inventario', login_url='')(CrearInventario), name='crear_inventario'),
    path('inventarios/listar_inventarios/',permission_required('personas.view_inventario', login_url='')(ListarInventarios), name='listar_inventarios'),
    path('inventarios/editar_inventarios/<int:id>',permission_required('personas.change_inventario', login_url='')(EditarInventario), name='editar_inventario'),
    path('inventarios/eliminar_inventarios/<int:id>',permission_required('personas.delete_inventario', login_url='')(EliminarInventario), name='eliminar_inventario'),


#SEGMENTO PARA REQUISICIONES
    #ES LA LIGA , LA FUNCION A DONDE VA ,  EL NOMBRE DEL DIRECCIONAMIENTO
    path('requisiciones/crear_requisicion/',permission_required('personas.add_requisicion', login_url='')(CrearRequisicion), name='crear_requisicion'),
    path('requisiciones/listar_requisiciones/',permission_required('personas.view_requisicion', login_url='')(ListarRequisiciones), name='listar_requisiciones'),
    path('requisiciones/editar_requisiciones/<int:id>',permission_required('personas.change_requisicion', login_url='')(EditarRequisicion), name='editar_requisicion'),
    path('requisiciones/imprimir_requisicion/<int:id>',permission_required('personas.view_requisicion', login_url='')(ImprimirRequisicion), name='imprimir-requisicion'),
    path('requisiciones/eliminar_requisiciones/<int:id>',permission_required('personas.delete_requisicion', login_url='')(EliminarRequisicion), name='eliminar_requisicion'),
    path('requisiciones/cancelar/<int:id>',permission_required('personas.change_requisicion', login_url='')(CancelarRequisicion), name='cancelar-requisicion'),
    path('requisiciones/deslistar/<int:id>',permission_required('personas.change_requisicion', login_url='')(TerminarRequisicion), name='delistar-requisicion'),

#SEGMENTO PARA ORDENES DE COMPRA
    path('ordenes/crear_orden/<int:id>',permission_required('personas.add_ordencompra', login_url='')(CrearOrden), name='crear_orden'),
    path('ordenes/listar_ordenes/',permission_required('personas.view_ordencompra', login_url='')(ListarOrdenes), name='listar_ordenes'),
    path('ordenes/editar_ordenes/<int:id>',permission_required('personas.change_ordencompra', login_url='')(EditarOrden), name='editar_orden'),
    path('ordenes/eliminar_orden/<int:id>',permission_required('personas.delete_ordencompra', login_url='')(EliminarOrden), name='eliminar_orden'),
    path('ordenes/cancelar/<int:id>',permission_required('personas.change_ordencompra', login_url='')(CancelarOrden), name='cancelar-orden'),
    path('ordenes/imprimir_orden/<int:id>',permission_required('personas.view_ordencompra', login_url='')(ImprimirOrden), name='imprimir-orden'),
    path('ordenes/contar_impresiones/<int:id>',permission_required('personas.view_ordencompra', login_url='')(ContadorImpresiones), name='contador_impresiones'),
#SEGMENTO PARA  COMPRA
    path('compras/crear_compra/<int:id>',permission_required('personas.add_compra', login_url='')(CrearCompra), name='crear_compra'),
    path('compras/listar_compras/',permission_required('personas.view_compra', login_url='')(ListarCompras), name='listar_compras'),
    path('compras/editar_compras/<int:id>',permission_required('personas.change_compra', login_url='')(EditarCompra), name='editar_compra'),
    path('compras/eliminar_compra/<int:id>',permission_required('personas.delete_compra', login_url='')(EliminarCompra), name='eliminar_compra'),
    path('compras/cancelar_compra/<int:id>',permission_required('personas.change_compra', login_url='')(CancelarCompra), name='cancelar_compra'),
    path('compras/terminar_compra/<int:id>',permission_required('personas.change_compra', login_url='')(TerminarCompra), name='terminar_compra'),
#SEGMENTO PARA LISTADO DE REPORTES
    path('reportes/requerimientos/',permission_required('personas.view_requisicion', login_url='')(ReporteRequerimientos), name='reporte_requerimientos'),
    path('reportes/ordenes_compra/',permission_required('personas.view_ordencompra', login_url='')(ReporteOrdenes), name='reporte_ordenes'),
    path('reportes/compras/',permission_required('personas.view_compra', login_url='')(ReporteCompras), name='reporte_compras'),
    path('reportes/vehiculos/',permission_required('personas.view_ordencompra', login_url='')(ReporteVehiculos), name='reporte_vehiculos'),

    path('sinpermisos/', SinPermisos, name='sin_permisos'),
    path('bitacora/', ListarBitacora, name='bitacora'),
#SEGMENTO PARA CONCEPTOS
    path('conceptos/crear_concepto/',permission_required('personas.add_concepto', login_url='')(CrearConcepto), name='crear_concepto'),
    path('conceptos/listar_conceptos/',permission_required('personas.view_concepto', login_url='')(ListarConceptos), name='listar_conceptos'),
    path('conceptos/editar_concepto/<int:id>',permission_required('personas.change_concepto', login_url='')(EditarConcepto), name='editar_concepto'),
    path('conceptos/eliminar_concepto/<int:id>',permission_required('personas.delete_concepto', login_url='')(EliminarConcepto), name='eliminar_concepto'),
#SEGMENTO PARA VENTAS
    path('ventas/crear_venta/',permission_required('personas.add_venta', login_url='')(CrearVenta), name='crear_venta'),
    path('ventas/listar_ventas/',permission_required('personas.view_venta', login_url='')(ListarVentas), name='listar_ventas'),
    path('ventas/editar_venta/<int:id>',permission_required('personas.change_venta', login_url='')(EditarVenta), name='editar_venta'),
    path('ventas/eliminar_venta/<int:id>',permission_required('personas.delete_venta', login_url='')(EliminarVenta), name='eliminar_venta'),
#SEGMENTO PARA VEHICULOS
    path('vehiculos/crear_vehiculo/',permission_required('personas.add_vehiculo', login_url='')(CrearVehiculo), name='crear_vehiculo'),
    path('vehiculos/listar_vehiculos/',permission_required('personas.view_vehiculo', login_url='')(ListarVehiculo), name='listar_vehiculos'),
    path('vehiculos/editar_vehiculo/<int:id>',permission_required('personas.change_vehiculo', login_url='')(EditarVehiculo), name='editar_vehiculo'),
    path('vehiculos/eliminar_vehiculo/<int:id>',permission_required('personas.delete_vehiculo', login_url='')(EliminarVehiculo), name='eliminar_vehiculo'),
#SEGMENTO PARA TIPOS DE VEHICULOS
    path('vehiculos/crear_tipovehiculo/',permission_required('personas.add_tiposvehiculo', login_url='')(CrearTiposVehiculo), name='crear_tiposvehiculo'),
    path('vehiculos/listar_tipovehiculoss/',permission_required('personas.view_tiposvehiculo', login_url='')(ListarTiposVehiculos), name='listar_tiposvehiculos'),
    path('vehiculos/editar_tipovehiculo/<int:id>',permission_required('personas.change_tiposvehiculo', login_url='')(EditarTiposVehiculo), name='editar_tiposvehiculo'),
    path('vehiculos/eliminar_tipovehiculo/<int:id>',permission_required('personas.delete_tiposvehiculo', login_url='')(EliminarTiposVehiculo), name='eliminar_tiposvehiculo'),

]

urlpatterns += [

    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT
    }),
    ]