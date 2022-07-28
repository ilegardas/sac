
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from personas.forms import DepartamentoForm, RecursoForm, ProductoForm, ProveedorForm, InventarioForm, RequisicionForm, \
    OrdenForm, CompraForm, UsuarioForm, ReporteRequisicionesForm, ReporteOrdenesForm, ReporteComprasForm, \
    UploadFileForm, ConceptoForm, VentaForm, VehiculoForm, TiposVehiculoForm, ProductosForm, ConceptosForm, \
    ReporteFechasForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from personas.models import Departamento, Recurso, Producto, Proveedor, Inventario, Requisicion, OrdenCompra, Compra, \
    Usuario, Bitacora, Concepto, Venta, Vehiculo, TiposVehiculo, ConceptoVenta
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import messages
import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@method_decorator(csrf_exempt)
@method_decorator(login_required)
def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
#Para actualizar el logo del formato de orden de compra
def handle_uploaded_file(f):
    with open('static/img/logo.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def cambiar_logo(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['Logotipo'])
            return redirect('inicio')
    else:
        form_logo = UploadFileForm()
    return render(request, 'logotipo/cambiar.html', {'form_logo': form_logo})


def ObtenUsuario(request):
    current_user = request.user
    usuario = current_user.nombres + " " + current_user.apellidos
    return usuario
def Notificar(request,asunto,mensaje,destinatario):
    if destinatario is not None:
        send_mail(
            asunto,
            mensaje,
            'sacmunicipio@gmail.com',
            destinatario,
            fail_silently=False,
        )
    else:
        pass

@login_required
def Home(request):

    requisicionesp = Requisicion.objects.filter(persona_id=request.user, estatus='pendiente').count()
    requisicionesc = Requisicion.objects.filter( persona_id=request.user, estatus='cancelada' ).count()
    requisicionesa = Requisicion.objects.filter( persona_id=request.user, estatus='procesado' ).count()

    return render(request, 'inicio/charts.html',{'requisicionesp':requisicionesp,'requisicionesc':requisicionesc,'requisicionesa':requisicionesa})

def salir(request):
    logout(request)
    messages.add_message(request=request,level=messages.SUCCESS,message="Se ha finalizado la sesion!")
    return redirect('/')

#pantalla para cuando no tengan permisos para determinada pagina
def SinPermisos(request):
    logout(request)
    messages.add_message( request=request, level=messages.SUCCESS, message="No tiene permisos para esta seccion" )
    return render(request, 'sin_permisos/sin_acceso.html')

#DEFINICION DE FUNCIONES PARA LOS DEPARTAMENTOS
@login_required
def CrearDepartamento(request):
    if request.user.has_perm("personas.add_departamento") == False:
        SinPermisos(request)
    if request.method == 'POST':

        nom = request.POST.get('nombre')
        desc = request.POST.get('descripcion')
        departamento = Departamento(nombre=nom,descripcion=desc)
        departamento.save()
        return redirect( 'listar_departamentos')
    else:
        departamento_form = DepartamentoForm()
    return render(request, 'departamentos/crear_departamento.html',{'departamento_form': departamento_form})
@login_required
def ListarDepartamentos(request):
    if request.user.has_perm("personas.view_departamento") == False:
        SinPermisos(request)
    departamentos = Departamento.objects.all()
    return render(request, 'departamentos/listar_departamentos.html', {'departamentos':departamentos})
@login_required
def EditarDepartamento(request, id):
    if request.user.has_perm("personas.change_departamento") == False:
        SinPermisos(request)
    departamento_form = None
    error = None
    try:
        departamento = Departamento.objects.get( id=id)

        if request.method == 'GET':
            departamento_form = DepartamentoForm(instance=departamento )
        else:
            departamento_form = DepartamentoForm( request.POST, instance=departamento )
            if departamento_form.is_valid():
                departamento_form.save()
            return redirect( 'listar_departamentos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'departamentos/crear_departamento.html', {'departamento_form': departamento_form,'error':error})
@login_required
def EliminarDepartamento(request,id):
    if request.user.has_perm("personas.delete_departamento") == False:
        SinPermisos(request)

    departamento = Departamento.objects.get(id=id)
    if request.method == 'POST':
        departamento.delete()
        return redirect('listar_departamentos')
    return render(request,'departamentos/eliminar_departamento.html', {'departamento':departamento})

#DEFINICION DE FUNCIONES PARA LOS RECURSOS
def CrearUsuario(request):
    grupos = Group.objects.all()
    if request.user.has_perm("personas.add_usuario") == False:
        SinPermisos(request)

        #Group.objects.get(name='my_group_name')
    if request.method == 'POST':
        grupo = request.POST.get( 'grupo' )
        username = request.POST.get( 'username' )
        clave = request.POST.get( 'password' )
        password = make_password( clave, salt=None, hasher='default' )
        email = request.POST.get( 'email' )
        nombres = request.POST.get( 'nombres' )
        apellidos = request.POST.get( 'apellidos' )
        departamento = Departamento.objects.get(id=request.POST.get( 'departamento_id' ) )
        telefono = request.POST.get( 'telefono' )
        if request.POST.get( 'is_active' ) == 'on':
            is_active = True
        else:
            is_active = False

        is_active = is_active
        if request.POST.get( 'is_staff' ) == 'on':
            is_staff = True
        else:
            is_staff = False
        is_staff = is_staff
        imagen = request.FILES.get('imagen')

        usuario =Usuario(
            username=username,
            password=password,
            email=email,
            nombres=nombres,
            apellidos=apellidos,
            departamento_id=departamento,
            imagen=imagen,
            telefono=telefono,
            is_active=is_active,
            is_staff=is_staff

        )
        valida = 0
        valida = Usuario.objects.filter(Q(email=usuario.email) | Q(username=usuario.username)).count()
        if valida == 0:
            usuario.save()
            messages.add_message( request=request, level=messages.SUCCESS, message="Usuario Creado Exitósamente" )
            my_group = Group.objects.get( name=grupo ) #obtenemos el grupo seleccionado de los permisos
            if my_group is not None: #Nos aseguramos que encuentre un valor
                my_group.user_set.add(usuario) # se agrega el nuevo usuario al grupo
        else:
            messages.add_message( request=request, level=messages.SUCCESS, message="No se pudo guardar. Ya existe un usuario con ese mail o usuario" )
        return redirect('listar_usuarios')
    else:
        usuario_form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html',{'usuario_form': usuario_form, 'grupos':grupos})

@login_required
def ListarUsuarios(request):
    if request.user.has_perm("personas.view_usuario") == False:
        SinPermisos(request)
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios':usuarios })

@login_required
def EditarUsuario(request, id):
    if request.user.has_perm("personas.change_usuario") == False:
        SinPermisos(request)
    grupos = Group.objects.all()
    usuario_form = None
    error = None
    my_group = None
    try:
        usuario = Usuario.objects.get( id=id)

        if request.method == 'GET':
            usuario_form = UsuarioForm( instance=usuario )
        else:
            grupo = request.POST.get('grupo')
            usuario.username = request.POST.get( 'username' )
            clave = request.POST.get( 'password' )
            if clave == usuario.password: #para no volver a codificar si no se ha modificado
                pass
            else:
                usuario.password = make_password(clave,salt=None,hasher='default')

            usuario.email = request.POST.get( 'email' )
            usuario.nombres = request.POST.get( 'nombres' )
            usuario.apellidos = request.POST.get( 'apellidos' )
            departamento = Departamento.objects.get(id=request.POST.get( 'departamento_id' ))
            usuario.departamento_id = departamento
            usuario.telefono=request.POST.get( 'telefono' )
            if request.POST.get( 'is_active' )=='on':
                is_active=True
            else:
                is_active=False

            usuario.is_active = is_active
            if request.POST.get( 'is_staff' )=='on':
                is_staff=True
            else:
                is_staff=False
            usuario.is_staff = is_staff
            usuario.imagen = request.FILES.get('imagen')
            usuario.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Usuario modificado exitósamente" )
            if len(grupo) > 2:
                my_group = Group.objects.get(name=grupo)  # obtenemos el grupo seleccionado de los permisos
            if my_group is not None:  # Nos aseguramos que encuentre un valor
                usuario.groups.clear()
                my_group.user_set.add( usuario )  # se agrega el nuevo usuario al grupo
            return redirect( 'listar_usuarios' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'usuarios/crear_usuario.html', {'usuario_form': usuario_form,'error':error,'grupos':grupos})
@login_required
def EliminarUsuario(request,id):
    if request.user.has_perm("personas.delete_usuario") == False:
        SinPermisos(request)
    usuario = Usuario.objects.get(id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.add_message( request=request, level=messages.SUCCESS, message="Usuario eliminado exitósamente!" )
        return redirect('listar_usuarios')
    return render(request,'usuarios/eliminar_usuario.html', {'usuario':usuario})


#DEFINICION DE FUNCIONES PARA LOS RECURSOS
def CrearRecurso(request):
    if request.user.has_perm("personas.add_recurso") == False:
        SinPermisos(request)
    if request.method == 'POST':
        recurso_form = RecursoForm(request.POST)
        if recurso_form.is_valid():
            recurso_form.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Recurso agregado correctamente: " + recurso_form.cleaned_data['nombre'] )
            return redirect('listar_recursos')
    else:
        recurso_form = RecursoForm()
    return render(request, 'recursos/crear_recurso.html',{'recurso_form': recurso_form})
@login_required
def ListarRecursos(request):
    if request.user.has_perm("personas.view_recurso") == False:
        SinPermisos(request)
    recursos = Recurso.objects.all()
    return render(request, 'recursos/listar_recursos.html', {'recursos':recursos })
@login_required
def EditarRecurso(request, id):
    if request.user.has_perm("personas.change_recurso") == False:
        SinPermisos(request)
    recurso_form = None
    error = None
    try:
        recurso = Recurso.objects.get( id=id)

        if request.method == 'GET':
            recurso_form = RecursoForm( instance=recurso )
        else:
            recurso_form = RecursoForm( request.POST, instance=recurso )

            print(recurso_form.vehiculo_id)
            if recurso_form.is_valid():
                recurso_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Recurso editado correctamente: " + recurso_form.cleaned_data['nombre'] )
            return redirect( 'listar_recursos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'recursos/crear_recurso.html', {'recurso_form': recurso_form,'error':error})
@login_required
def EliminarRecurso(request,id):
    if request.user.has_perm("personas.delete_recurso") == False:
        SinPermisos(request)
    recurso = Recurso.objects.get(id=id)
    if request.method == 'POST':
        recurso.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Recurso eliminado correctamente: " + recurso.nombre )
        return redirect('listar_recursos')
    return render(request,'recursos/eliminar_recurso.html', {'recurso':recurso})


#DEFINICION DE FUNCIONES PARA LOS PRODUCTOS
@login_required
def CrearProducto(request):
    if request.user.has_perm("personas.add_producto") == False:
        SinPermisos(request)
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        if producto_form.is_valid():
            producto_form.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Producto agregado correctamente: " + producto_form.cleaned_data['nombre'] )
            return redirect('listar_productos')
    else:
        producto_form = ProductoForm()
    return render(request, 'productos/crear_producto.html',{'producto_form': producto_form})
@login_required
def ListarProductos(request):
    if request.user.has_perm("personas.view_producto") == False:
        SinPermisos(request)
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos':productos})
@login_required
def EditarProducto(request, id):
    if request.user.has_perm("personas.change_producto") == False:
        SinPermisos(request)
    producto_form = None
    error = None
    try:
        producto = Producto.objects.get( id=id)

        if request.method == 'GET':
            producto_form = ProductoForm( instance=producto )
        else:
            producto_form = ProductoForm( request.POST, instance=producto )
            if producto_form.is_valid():
                producto_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Producto editado correctamente: " + producto_form.cleaned_data[
                                          'nombre'] )

                return redirect( 'listar_productos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'productos/crear_producto.html', {'producto_form': producto_form,'error':error})
@login_required
def EliminarProducto(request,id):
    if request.user.has_perm("personas.delete_producto") == False:
        SinPermisos(request)
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        producto.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Producto eliminado correctamente: " + producto.nombre )
        return redirect('listar_productos')
    return render(request,'productos/eliminar_producto.html', {'producto':producto})
def ProductoEnUso(request,id):
    producto = Producto.objects.get( id=id )
    producto.en_uso='si'
    producto.save()
    return 'Producto Modificado'
def ProductoSinUso(request,id):
    producto = Producto.objects.get( id=id )
    req=0
    req = Requisicion.objects.filter(producto_id=producto.id).count()
    print(req)
    if req < 2:
        producto.en_uso='no'
        producto.save()
        return 'Producto Modificado'
    return 'Producto no Modificado'
#DEFINICION DE FUNCIONES PARA LOS PROVEEDORES
@login_required
def CrearProveedor(request):
    if request.user.has_perm("personas.add_proveedor") == False:
        SinPermisos(request)
    if request.method == 'POST':
        proveedor_form = ProveedorForm(request.POST)
        if proveedor_form.is_valid():
            proveedor_form.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Proveedor agregado correctamente: " + proveedor_form.cleaned_data['nombre'] )
            return redirect('listar_proveedores')
    else:
        proveedor_form = ProveedorForm()
    return render(request, 'proveedores/crear_proveedor.html',{'proveedor_form': proveedor_form})
@login_required
def ListarProveedores(request):
    if request.user.has_perm("personas.view_proveedor") == False:
        SinPermisos(request)
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/listar_proveedores.html', {'proveedores':proveedores})
@login_required
def EditarProveedor(request, id):
    if request.user.has_perm("personas.change_proveedor") == False:
        SinPermisos(request)
    proveedor_form = None
    error = None
    try:
        proveedor = Proveedor.objects.get( id=id)

        if request.method == 'GET':
            proveedor_form = ProveedorForm( instance=proveedor )
        else:
            proveedor_form = ProveedorForm( request.POST, instance=proveedor )
            if proveedor_form.is_valid():
                proveedor_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Proveedor editado correctamente: " + proveedor_form.cleaned_data['nombre'] )
            return redirect( 'listar_proveedores' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'proveedores/crear_proveedor.html', {'proveedor_form': proveedor_form,'error':error})
@login_required
def EliminarProveedor(request,id):
    if request.user.has_perm("personas.delete_proveedor") == False:
        SinPermisos(request)
    proveedor = Proveedor.objects.get(id=id)
    if request.method == 'POST':
        proveedor.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Proveedor eliminado correctamente: " + proveedor.nombre )
        return redirect('listar_proveedores')
    return render(request,'proveedores/eliminar_proveedor.html', {'proveedor':proveedor})

#DEFINICION DE FUNCIONES PARA LOS INVENTARIOS
@login_required
def CrearInventario(request):
    if request.user.has_perm("personas.add_inventario") == False:
        SinPermisos(request)
    if request.method == 'POST':
        inventario_form = InventarioForm(request.POST)
        if inventario_form.is_valid():
            inventario_form.save()
            bitacora = Bitacora(fecha_creacion=datetime.now(),folio = str(inventario_form.cleaned_data['producto_id']) +"("+ str(inventario_form.cleaned_data['stock']) + ")",estatus="Inventario Creado",usuario=request.user.nombres,tipo_documento="inventario")
            bitacora.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Inventario agregado correctamente: " + inventario_form.cleaned_data['descripcion'] )
            return redirect('listar_inventarios')
    else:
        inventario_form = InventarioForm()
    return render(request, 'inventarios/crear_inventario.html',{'inventario_form': inventario_form})
@login_required
def ListarInventarios(request):
    if request.user.has_perm("personas.view_inventario") == False:
        SinPermisos(request)
    inventarios = Inventario.objects.all()
    return render(request, 'inventarios/listar_inventarios.html', {'inventarios':inventarios})
@login_required
def EditarInventario(request, id):
    if request.user.has_perm("personas.change_inventario") == False:
        SinPermisos(request)
    inventario_form = None
    error = None
    try:
        inventario = Inventario.objects.get(id=id)

        if request.method == 'GET':
            inventario_form = InventarioForm( instance=inventario )
        else:
            inventario_form = InventarioForm( request.POST, instance=inventario )
            if inventario_form.is_valid():
                inventario_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Inventario editado correctamente: " + inventario_form.cleaned_data[
                                          'descripcion'] )
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( inventario_form.cleaned_data['producto_id'] ) + "(" + str(
                                         inventario_form.cleaned_data['stock'] ) + ")",
                                     estatus="Inventario Editado",
                                     usuario=request.user.nombres,
                                     tipo_documento="inventario" )
                bitacora.save()
            return redirect( 'listar_inventarios' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'inventarios/crear_inventario.html', {'inventario_form': inventario_form,'error':error})
@login_required
def EliminarInventario(request,id):
    if request.user.has_perm("personas.delete_inventario") == False:
        SinPermisos(request)
    inventario = Inventario.objects.get(id=id)
    if request.method == 'POST':
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( inventario.producto_id ) + "(" + str(
                                 inventario.stock ) + ")",
                             estatus="Inventario Eliminado",
                             usuario=request.user.nombres, tipo_documento="inventario" )
        bitacora.save()
        inventario.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Inventario eliminado correctamente: " + inventario.descripcion )
        return redirect('listar_inventarios')
    return render(request, 'inventarios/eliminar_inventario.html', {'inventario':inventario})

#DEFINICION DE FUNCIONES PARA LAS REQUISICIONES
@login_required
def CrearRequisicion(request):
    usuario = request.user
    if request.user.has_perm("personas.add_requisicion") == False:
        SinPermisos(request)
    if request.method == 'POST':
        #Obtengo la lista de productos
        producto = Producto.objects.filter(id__in=request.POST.getlist('productos'))
        if (request.POST.get('vehiculos') != ""):
            vehiculo = Vehiculo.objects.get(id=request.POST.get('vehiculos'))
        else:
            vehiculo = None

        if (request.POST.get('departamentos') == ""):
            departamento = usuario.departamento_id
        else:
            departamento = Departamento.objects.get( id=request.POST.get( 'departamentos' ) )

        persona = request.user
        recursos_id = Recurso.objects.get(id=request.POST.get('recursos_id'))
        proveedor_id = Proveedor.objects.get( id=request.POST.get( 'proveedor_id' ) )
        descripcion = request.POST.get('descripcion')
        fecha_creacion = datetime.now()
        fecha_estatus = datetime.now()
        estatus = 'pendiente'

        requisicion = Requisicion(
            departamento_id=departamento,
            persona_id=persona,
            recursos_id=recursos_id,
            proveedor_id=proveedor_id,
            vehiculo_id=vehiculo,
            descripcion=descripcion,
            estatus=estatus,
            fecha_creacion = fecha_creacion,
            fecha_estatus = fecha_estatus,

        )

        requisicion.save()
        for prod in producto:
            requisicion.producto_id.add(prod.id)
            ProductoEnUso(request, prod.id)
        requisicion.save()
        #SE AGREGA MOVIMIENTO A LA BITACORA
        pedido = ""
        for prods in requisicion.producto_id.all():
            pedido = pedido + str(prods.nombre) +","
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Requerimiento creado correctamente: " + requisicion.descripcion )

        #SE ENVIA CORREO DE NOTIFICACION DE REQUERIMIENTO CREADO HACIA LOS APROBADORES
        aprobadores_mail = []
        aprobadores = Usuario.objects.filter( groups__name__in=['Aprobador'] )
        for aprobador in aprobadores:
            aprobadores_mail.append( aprobador.email )
        mensaje = "Se ha creado un requerimiendo solicitando: " + str(pedido) + " " + str(requisicion.descripcion) + ", creado por:" + str(requisicion.persona_id) + " del departamento de: " + str(requisicion.departamento_id)
        #Notificar(request,'creacion de requerimiento',mensaje,aprobadores_mail)
        #SE GUARDA A LA BITACORA LA REQUISICION CREADA
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio= "(" + str(
                                 pedido ) + ")",
                             estatus="Requerimiento Creado",
                             usuario=request.user.nombres,
                             tipo_documento="Requerimiento" )
        bitacora.save()

        #SE REDIRECCIONA A LA LISTA DE REQUERIMIENTOS DEL USUARIO
        return redirect('listar_requisiciones')
    else:
        requisicion_form = RequisicionForm(user=request.user)
        catalogos_form = ProductosForm()
        departamentos = Departamento.objects.all()

        #if request.user.groups.all()[0].name == "SuperAdmins": este nombre solo esta en esta  lap
        if request.user.groups.all()[0].name == "superadmin":
            vehiculos = Vehiculo.objects.filter( visible='si' )
        else:
            vehiculos = Vehiculo.objects.filter(visible='si',departamento_id=request.user.departamento_id.id)
        grupo = request.user.groups.all()[0].name
    return render(request, 'requisiciones/crear_requisicion.html',{'requisicion_form': requisicion_form,'usuario':usuario,'catalogos_form':catalogos_form,'vehiculos':vehiculos, 'departamentos':departamentos, 'grupo':grupo})
@login_required
def ListarRequisiciones(request):

    if request.user.has_perm( "personas.view_requisicion" ) == False:
        SinPermisos( request )
    requisiciones = Requisicion.objects.filter(persona_id=request.user).exclude(listar='no').order_by('-pk')
    return render(request, 'requisiciones/listar_requisiciones.html', {'requisiciones':requisiciones})
@login_required
def EditarRequisicion(request, id):
    if request.user.has_perm("personas.change_requisicion") == False:
        SinPermisos(request)
    usuario = ObtenUsuario( request )
    requisicion_form = None
    error = None
    try:
        requisicion = Requisicion.objects.get(id=id)


        if request.method == 'GET':
            requisicion_form = RequisicionForm(instance=requisicion, user=request.user)
            departamentos = Departamento.objects.all()
            grupo = request.user.groups.all()[0].name
            departamento = requisicion.departamento_id.id
        else:
            producto = None
            requisicion_form = RequisicionForm(request.POST, instance=requisicion, user=request.user)
            requisicion = Requisicion.objects.get(id=requisicion.id)
            requisicion.descripcion = request.POST.get('descripcion')
            requisicion.recursos_id = Recurso.objects.get(id=request.POST.get('recursos_id'))
            requisicion.proveedor_id = Proveedor.objects.get( id=request.POST.get( 'proveedor_id' ) )

            if (request.POST.get( 'departamentos' ) != ""):
                requisicion.departamento_id = Departamento.objects.get( id=request.POST.get( 'departamentos' ) )

            #requisicion.vehiculo_id = Vehiculo.objects.get( id=request.POST.get( 'vehiculo_id' ) )

            if (request.POST.get( 'vehiculo_id' ) is not None) :

                if (request.POST.get( 'vehiculo_id' ) == ""):
                    requisicion.vehiculo_id = None
                else:
                    requisicion.vehiculo_id = Vehiculo.objects.get( id=request.POST.get( 'vehiculo_id' ) )
            else:
                vehiculo = None
            requisicion.save()
            #Se agregan los productos a la requisicion
            producto = Producto.objects.filter( id__in=request.POST.getlist( 'producto_id' ) )
            if producto is not None:
                requisicion.producto_id.clear()
                for prod in producto:
                    requisicion.producto_id.add( prod.id )
                    ProductoEnUso( request, prod.id )

            requisicion.save()
            pedido = ""
            for prods in requisicion.producto_id.all():
                pedido = pedido + str( prods.nombre ) + ","
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Requerimiento editado correctamente: " + requisicion.descripcion )
            bitacora = Bitacora( fecha_creacion=datetime.now(),
                                 folio= "(" + str(
                                     pedido ) + ")",
                                 estatus="Requerimiento Editado",
                                 usuario=request.user.nombres,
                                 tipo_documento="Requerimiento" )
            bitacora.save()

            return redirect('listar_requisiciones')
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'requisiciones/crear_requisicion_backup.html', {'requisicion_form': requisicion_form,'error':error,'usuario':usuario, 'requisicion':requisicion,'departamentos':departamentos, 'grupo':grupo, 'departamento_actual':departamento})
@login_required
def EliminarRequisicion(request,id):
    if request.user.has_perm("personas.delete_requisicion") == False:
        SinPermisos(request)
    usuario = ObtenUsuario( request )
    requisicion = Requisicion.objects.get(id=id)
    if request.method == 'POST':
        pedido = ""
        for prods in requisicion.producto_id.all():
            ProductoSinUso(request,prods.id)
            pedido = pedido + str( prods.nombre ) + ","

        requisicion.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Requerimiento eliminado correctamente: " + requisicion.descripcion )
        #Se guarda en la bitacora
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio= "(" + str(
                                 pedido ) + ")",
                             estatus="Requerimiento Eliminado",
                             usuario=request.user.nombres,
                             tipo_documento="Requerimiento" )
        bitacora.save()
        return redirect('listar_requisiciones')
    return render(request, 'requisiciones/eliminar_requisicion.html', {'requisicion':requisicion,'usuario':usuario})
@login_required
def CancelarRequisicion(request,id):
    if request.user.has_perm("personas.change_requisicion") == False:
        SinPermisos(request)
    requisicion = Requisicion.objects.get(id=id)
    requisicion.estatus = 'cancelado'
    requisicion.fecha_estatus = datetime.now()
    requisicion.save()
    pedido = ""
    for prods in requisicion.producto_id.all():
        pedido = pedido + str( prods.nombre ) + ","
    messages.add_message( request=request, level=messages.SUCCESS,
                          message="Requerimiento cancelado correctamente: " + requisicion.descripcion )
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio= "(" + str(
                             pedido ) + ")",
                         estatus="Requerimiento Cancelado",
                         usuario=request.user.nombres,
                         tipo_documento="Requerimiento" )
    bitacora.save()
    return redirect('listar_ordenes')
#CODIGO PARA MANDAR IMPRIMIR LA REQUISICION
def ImprimirRequisicion(request,id):
    if request.user.has_perm("personas.view_requisicion") == False:
        SinPermisos(request)
    requisicion = None
    fecha = datetime.now()
    requisicion = Requisicion.objects.get(id=id)
    return render(request, 'requisiciones/imprimir_requisicion.html', {'requisicion': requisicion,'fecha':fecha} )
#ESTA FUNCION CAMBIA EL ESTATUS DE LA FUNCION PARA NO PODER SER ELIMINADA EN EL LISTADO
@login_required
def OrdenDeRequisicion(request,id):
    requisicion = Requisicion.objects.get(id=id)
    requisicion.estatus = 'procesado'
    requisicion.fecha_estatus = datetime.now()
    requisicion.save()
    return ('generado')
#ESTA FUNCION CAMBIA EL ESTATUS DE LA FUNCION PARA NO PODER SER ELIMINADA EN EL LISTADO
@login_required
def TerminarRequisicion(request,id):
    requisicion = Requisicion.objects.get(id=id)
    requisicion.listar = 'no'
    requisicion.fecha_estatus = datetime.now()
    requisicion.save()
    return redirect( 'listar_requisiciones' )
#ESTA FUNCION REGRESA EL ESTATUS A PENDIENTE CUANDO SE ELIMINE UNA ORDEN DE COMPRA
@login_required
def LiberarRequisicion(request,id):
    requisicion = Requisicion.objects.get(id=id)
    requisicion.estatus = 'pendiente'
    requisicion.fecha_estatus = datetime.now()
    requisicion.save()
    return ('generado')

#DEFINICION DE VISTAS PARA LAS COMPRAS
@login_required
def CrearOrden(request,id=None):
    if request.user.has_perm("personas.add_ordencompra") == False:
        SinPermisos(request)
    usuario = request.user
    requisicion=None
    if id is not None:
        requisicion = Requisicion.objects.get(id=id)
    else:
        id=None
    if requisicion.estatus != "procesado":

        if request.method == 'POST':
            requerimiento_id = requisicion
            aprobador_id = usuario
            recursos_id = Recurso.objects.get(id=request.POST.get('recursos_id') )
            proveedor_id = Proveedor.objects.get(id=request.POST.get('proveedor_id'))
            descripcion = requisicion.descripcion
            estatus = 'autorizado'
            cantidad = request.POST.get('cantidad_prod')
            precio_unitario = request.POST.get('precio_unitario')
            precio_total = request.POST.get('precio_total')

            orden = OrdenCompra(
                requerimiento_id=requerimiento_id,
                aprobador_id=aprobador_id,
                recursos_id=recursos_id,
                proveedor_id=proveedor_id,
                cantidad_prod=cantidad,
                precio_unitario=precio_unitario,
                precio_total=precio_total,
                descripcion=descripcion,
                estatus=estatus,
                fecha_creacion=datetime.now(),
                fecha_estatus=datetime.now()

            )

            orden.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Orden creada correctamente: " + orden.descripcion )
            cambiado = OrdenDeRequisicion(request, requerimiento_id.id)
            #SE AGREGA A LA BITACORA
            pedido = ""
            for prods in requisicion.producto_id.all():
                pedido = pedido + str(prods.nombre) +","

            bitacora = Bitacora( fecha_creacion=datetime.now(),
                                 folio=str( orden.proveedor_id ) + "(" + str(
                                     pedido ) +" " + str(
                                     orden.cantidad_prod ) + ")",
                                 estatus="Orden Creada",
                                 usuario=request.user.nombres,
                                 tipo_documento="Orden de Compra" )
            bitacora.save()
            #SE NOTIFICA A LOS REQUISITORES POR CORREO
            destinatario = (requisicion.persona_id.email,)
            mensaje = "Se ha aprobado su solicitud de compra con descripción: " + str( pedido ) + ", " + str( requisicion.descripcion )
            #Notificar( request, 'Aprobacion de requerimiento', mensaje, destinatario )
            return redirect('listar_ordenes')
        else:
            orden_form = OrdenForm()
            recursos = Recurso.objects.filter(visible='si').order_by('nombre')
            proveedores = Proveedor.objects.all()
    else:
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Esta requisición ya se había autorizado anteriormente: " + str(requisicion.id) + ": " + requisicion.descripcion )
        return redirect( 'listar_ordenes' )


    return render(request, 'ordenes/crear_orden.html',{'orden_form': orden_form,'usuario':usuario,'requisicion':requisicion,'recursos':recursos,'proveedores':proveedores })

@login_required
def ListarOrdenes(request):
    if request.user.has_perm("personas.view_ordencompra") == False:
        SinPermisos(request)
    requisiciones_l = None
    ordenes_l = None
    requisiciones_l = Requisicion.objects.filter( estatus='pendiente' ).order_by('-pk')
    #AQUI SOLICITO VALO EL 11 04 2022 QUE TODOS PUEDAN VER LAS AUTORIZADOS DE TODOS
    #ordenes_l = OrdenCompra.objects.filter( aprobador_id=request.user, estatus='autorizado' ).order_by('-pk')
    startdate = datetime.today()
    enddate = startdate + timedelta(days=7)
    #Sample.objects.filter(date__range=[startdate, enddate])
    #ordenes_l = OrdenCompra.objects.filter( estatus='autorizado').order_by('-pk')
    ordenes_l = OrdenCompra.objects.filter( estatus='autorizado',fecha_creacion__range=[startdate, enddate] ).order_by('-pk')

    return render(request, 'ordenes/listar_ordenes.html', {'requisiciones':requisiciones_l,'ordenes': ordenes_l})
@login_required
def EditarOrden(request, id):
    if request.user.has_perm("personas.change_ordencompra") == False:
        SinPermisos(request)
    #orden_form = None
    error = None
    try:
        ordenc = OrdenCompra.objects.get(id=id)

        if request.method == 'GET':
            ordenc_form = OrdenForm(instance=ordenc)
            recursos = Recurso.objects.all()
            proveedores = Proveedor.objects.all()
        else:
            orden_form = OrdenForm( request.POST, instance=ordenc )
            orden = OrdenCompra.objects.get(id=ordenc.id)
            orden.recursos_id = Recurso.objects.get(id=request.POST.get('recursos_id'))
            orden.proveedor_id = Proveedor.objects.get( id=request.POST.get( 'proveedor_id' ) )
            orden.cantidad_prod = request.POST.get('cantidad_prod')
            orden.precio_unitario = request.POST.get('precio_unitario')
            orden.precio_total = request.POST.get('precio_total')
            orden.descripcion = request.POST.get('descripcion')

            if orden_form.is_valid():
                orden_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Orden editada correctamente: " + orden_form.cleaned_data['descripcion'] )
                #SE AGREGA EL MOVIMIENTO A LA BITACORA
                pedido = ""
                for prods in orden.requerimiento_id.producto_id.all():
                    pedido = pedido + str( prods.nombre ) + ","
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( orden_form.cleaned_data['proveedor_id'] ) + "(" + str(
                                         pedido ) + str(
                                         orden_form.cleaned_data['cantidad_prod'] ) + ")",
                                     estatus="Orden Editada",
                                     usuario=request.user.nombres,
                                     tipo_documento="Orden de Compra" )
                bitacora.save()
            return redirect( 'listar_ordenes' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'ordenes/editar_orden.html', {'ordenc_form': ordenc_form,'error':error,'orden':ordenc,'recursos':recursos,'proveedores':proveedores})
@login_required
def EliminarOrden(request,id):
    if request.user.has_perm("personas.delete_ordencompra") == False:
        SinPermisos(request)
    usuario = ObtenUsuario( request )
    orden = OrdenCompra.objects.get(id=id)
    if request.method == 'POST':
        cambiado = LiberarRequisicion( request, orden.requerimiento_id.id )
        orden.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Orden eliminada correctamente: " + orden.descripcion )
        # SE AGREGA EL MOVIMIENTO A LA BITACORA
        pedido = ""
        for prods in orden.requerimiento_id.producto_id.all():
            pedido = pedido + str( prods.nombre ) + ","
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( orden.proveedor_id ) + "(" + str(
                                 pedido ) + str(
                                 orden.cantidad_prod ) + ")",
                             estatus="Orden Eliminada",
                             usuario=request.user.nombres,
                             tipo_documento="Orden de Compra" )
        bitacora.save()
        return redirect('listar_ordenes')
    return render(request, 'ordenes/eliminar_orden.html', {'orden':orden,'usuario':usuario})
@login_required
def CancelarOrden(request,id):
    if request.user.has_perm("personas.change_ordencompra") == False:
        SinPermisos(request)
    orden = OrdenCompra.objects.get(id=id)
    orden.estatus = 'cancelado'
    orden.fecha_estatus = datetime.now()
    orden.save()
    messages.add_message( request=request, level=messages.SUCCESS,
                          message="Orden cancelada correctamente: " + orden.descripcion )
    # SE AGREGA EL MOVIMIENTO A LA BITACORA
    pedido = ""
    for prods in orden.requerimiento_id.producto_id.all():
        pedido = pedido + str( prods.nombre ) + ","
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( orden.proveedor_id ) + "(" + str(
                             pedido ) + str(
                             orden.cantidad_prod ) + ")",
                         estatus="Orden Cancelada",
                         usuario=request.user.nombres,
                         tipo_documento="Orden de Compra" )
    bitacora.save()
    return redirect('listar_ordenes')
@login_required
def ImprimirOrden(request,id):
    if request.user.has_perm("personas.view_ordencompra") == False:
        SinPermisos(request)
    orden = None
    requisicion = None
    fecha = datetime.now()
    orden = OrdenCompra.objects.get(id=id)
    #fecha = orden.fecha_creacion
    contador = ContadorImpresiones(request,id )
    requisicion = Requisicion.objects.get(id=orden.requerimiento_id.id)
    return render(request, 'ordenes/imprimir_ordenes.html', {'requisicion': requisicion, 'orden': orden,'fecha':fecha} )
@login_required
def ContadorImpresiones(request,id):
    orden = OrdenCompra.objects.get( id=id )
    orden.impresa = int(orden.impresa) + 1
    orden.save()
    print('se imprimio')
    return ('agregado')
@login_required
def LiberarOrden(request,id):
    orden = OrdenCompra.objects.get(id=id)
    orden.estatus = 'pendiente'
    orden.fecha_estatus = datetime.now()
    orden.save()
    return ('generado')
@login_required
def OrdenaCompra(request,id):
    orden = OrdenCompra.objects.get(id=id)
    orden.estatus = 'procesado'
    orden.fecha_estatus = datetime.now()
    orden.save()
    return ('generado')


#DEFINICION DE VISTAS PARA LAS COMPRAS
@login_required
def CrearCompra(request,id=None):
    if request.user.has_perm("personas.add_compra") == False:
        SinPermisos(request)
    usuario = request.user
    orden=None
    if id is not None:
        orden = OrdenCompra.objects.get(id=id)
    else:
        id=None

    if request.method == 'POST':

        ordenCompra_id = orden
        aprobador_id = usuario
        descripcion = request.POST.get('descripcion')
        pdf = request.FILES.get('pdf')
        xml = request.FILES.get('xml')

        Total = request.POST.get('Total')
        estatus = request.POST.get('estatus')

        compra = Compra(
            ordenCompra_id=ordenCompra_id,
            aprobador_id=aprobador_id,
            descripcion=descripcion,
            pdf=pdf,
            xml=xml,
            Total=Total,
            estatus=estatus,
            fecha_creacion=datetime.now(),
            fecha_estatus=datetime.now()

        )

        compra.save()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Compra creada correctamente: " + compra.descripcion )
        # SE AGREGA EL MOVIMIENTO A LA BITACORA
        pedido = ""
        for prods in compra.ordenCompra_id.requerimiento_id.producto_id.all():
            pedido = pedido + str( prods.nombre ) + ","
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                 pedido ) + str(
                                 compra.ordenCompra_id.cantidad_prod ) + ")",
                             estatus="Compra Creada",
                             usuario=request.user.nombres,
                             tipo_documento="Compra" )
        bitacora.save()
        cambiado = OrdenaCompra(request, compra.ordenCompra_id.id)
        return redirect('listar_compras')
    else:
        compra_form = CompraForm()

    return render(request, 'compras/crear_compra.html',{'compra_form': compra_form,'usuario':usuario,'orden':orden})

@login_required
def ListarCompras(request):
    if request.user.has_perm("personas.view_compra") == False:
        SinPermisos(request)
    ordenes = None
    compras = None
    valores = ('pendiente,pagado')
    ordenes = OrdenCompra.objects.filter(Q(estatus = 'autorizado')).order_by('-pk')
    compras = Compra.objects.filter(Q(estatus = 'pendiente') | Q(estatus='pagado')).order_by('-pk')
    return render(request, 'compras/listar_compras.html', {'ordenes':ordenes, 'compras':compras})
@login_required
def EditarCompra(request, id):
    if request.user.has_perm("personas.change_compra") == False:
        SinPermisos(request)
    compra_form = None
    error = None
    try:
        compra = Compra.objects.get( id=id)
        ordenc = OrdenCompra.objects.get(id=compra.ordenCompra_id.id)

        if request.method == 'GET':
            compra_form = CompraForm( instance=compra )
        else:
            compra_form = CompraForm( request.POST,request.FILES, instance=compra )
            if compra_form.is_valid():
                compra_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Compra editada correctamente: " + compra_form.cleaned_data['descripcion'] )
                # SE AGREGA EL MOVIMIENTO A LA BITACORA
                pedido = ""
                for prods in compra.ordenCompra_id.requerimiento_id.producto_id.all():
                    pedido = pedido + str( prods.nombre ) + ","
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                         pedido ) + str(
                                         compra.ordenCompra_id.cantidad_prod ) + ")",
                                     estatus="Compra Editada",
                                     usuario=request.user.nombres,
                                     tipo_documento="Compra" )
                bitacora.save()
            return redirect('listar_compras')
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'compras/crear_compra.html', {'compra_form': compra_form,'error':error,'orden':ordenc})
@login_required
def EliminarCompra(request,id):
    if request.user.has_perm("personas.delete_compra") == False:
        SinPermisos(request)
    usuario = request.user
    compra = Compra.objects.get(id=id)
    if request.method == 'POST':
        cambiado = LiberarOrden( request, compra.ordenCompra_id.id )
        compra.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Compra eliminada correctamente: " + compra.descripcion )
        # SE AGREGA EL MOVIMIENTO A LA BITACORA
        pedido = ""
        for prods in compra.ordenCompra_id.requerimiento_id.producto_id.all():
            pedido = pedido + str( prods.nombre ) + ","
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                 pedido ) + str(
                                 compra.ordenCompra_id.cantidad_prod ) + ")",
                             estatus="Compra Eliminada",
                             usuario=request.user.nombres,
                             tipo_documento="Compra" )
        bitacora.save()
        return redirect('listar_compras')
    return render(request, 'compras/eliminar_compra.html', {'compra':compra,'usuario':usuario})
@login_required
def CancelarCompra(request,id):
    if request.user.has_perm("personas.change_compra") == False:
        SinPermisos(request)
    compra = Compra.objects.get(id=id)
    compra.estatus = 'cancelado'
    compra.fecha_estatus = datetime.now()
    compra.save()
    # SE AGREGA EL MOVIMIENTO A LA BITACORA
    pedido = ""
    for prods in compra.ordenCompra_id.requerimiento_id.producto_id.all():
        pedido = pedido + str( prods.nombre ) + ","
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                             pedido ) + str(
                             compra.ordenCompra_id.cantidad_prod ) + ")",
                         estatus="Compra Cancelada",
                         usuario=request.user.nombres,
                         tipo_documento="Compra" )
    bitacora.save()
    return redirect('listar_compras')

@login_required
def TerminarCompra(request,id):
    if request.user.has_perm("personas.change_compra") == False:
        SinPermisos(request)
    compra = Compra.objects.get(id=id)
    compra.estatus = 'terminado'
    compra.fecha_estatus = datetime.now()
    compra.save()
    # SE AGREGA EL MOVIMIENTO A LA BITACORA
    pedido = ""
    for prods in compra.ordenCompra_id.requerimiento_id.producto_id.all():
        pedido = pedido + str( prods.nombre ) + ","
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                             pedido ) + str(
                             compra.ordenCompra_id.cantidad_prod ) + ")",
                         estatus="Compra Terminada",
                         usuario=request.user.nombres,
                         tipo_documento="Compra" )
    bitacora.save()
    return redirect('listar_compras')

@login_required
def ReporteRequerimientos(request):
    if request.user.has_perm( "personas.view_ordencompra" ) == False:
        SinPermisos( request )

    ReporteRequisicion_form = None
    error = None
    requisicion = Requisicion()
    departamentos = Departamento.objects.all()
    personas = Usuario.objects.all()
    productos = Producto.objects.all()

    if request.method == 'GET':
        ReporteRequisicion_form = ReporteRequisicionesForm( instance=requisicion )
        requisiciones = Requisicion.objects.all()
        return render( request,
                       'reporte_requisiciones/listar_requisiciones.html',
                       {#'requisiciones': requisiciones,
                        'ReporteRequisicion_form': ReporteRequisicion_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos} )
    else:

        Query = Requisicion.objects.filter( descripcion__contains=request.POST.get( 'descripcion' ))
        fecha_creacion = request.POST.get( 'fecha_creacion' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter( fecha_creacion__range=[fecha_i, fecha_f] )

        if request.POST.get( 'departamento_id' ) != 'todos':
            Query = Query.filter( departamento_id=request.POST.get( 'departamento_id' ) )

        if request.POST.get( 'producto_id' ) != 'todos':
            producto = Producto.objects.filter( id=request.POST.get( 'producto_id' ) )
            Query = Query.filter(producto_id__in=producto)

        if request.POST.get( 'persona_id' ) != 'todos':
            Query = Query.filter( persona_id=request.POST.get( 'persona_id' ))

        if request.POST.get( 'estatus' ) != 'todos':
            Query = Query.filter(estatus=request.POST.get( 'estatus' ))

        Query = Query.order_by('-pk')
        requisiciones = Query
        return render(
            request,
            'reporte_requisiciones/listar_requisiciones.html',

                       {''
                        'requisiciones': requisiciones,
                        'ReporteRequisicion_form': ReporteRequisicion_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos
                        } )

@login_required
def ReporteOrdenes(request):
    if request.user.has_perm("personas.view_ordencompra") == False:
        SinPermisos(request)
    ReporteOrden_form = None
    error = None
    orden = OrdenCompra()
    departamentos = Departamento.objects.all()
    personas = Usuario.objects.all()
    productos = Producto.objects.all()
    recursos = Recurso.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'GET':
        ReporteOrden_form = ReporteOrdenesForm( instance=orden )
        ordenes = OrdenCompra.objects.all()
        return render( request,
                       'reportes_ordenes/listar_ordenes.html',
                       {#'ordenes': ordenes,
                        'ReporteOrden_form': ReporteOrden_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos,
                        'recursos':recursos,
                        'proveedores':proveedores} )
    else:

        fecha_creacion = request.POST.get( 'fecha_creacion',None)
        descripcion = request.POST.get( 'descripcion' )


        Query = OrdenCompra.objects.filter(descripcion__contains=descripcion)
        #producto = request.POST.get( 'producto_id' )
        recurso = request.POST.get( 'recurso_id' )
        usuario = request.POST.get( 'aprobador_id' )
        proveedor = request.POST.get( 'proveedor_id' )
        estatus = request.POST.get( 'estatus' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter(fecha_creacion__range=[fecha_i, fecha_f] )

        if request.POST.get( 'producto_id' ) != 'todos':
            producto = Producto.objects.filter( id=request.POST.get( 'producto_id' ) )
            req = None
            req = Requisicion.objects.filter(producto_id__in=producto)
            Query = Query.filter( requerimiento_id__in=req )

        if request.POST.get( 'departamento_id' ) != 'todos':
            dep = Departamento.objects.get( id=request.POST.get( 'departamento_id' ) )
            req = None
            req = Requisicion.objects.filter( departamento_id=dep.id )
            Query = Query.filter(requerimiento_id__in=req)

        if recurso != 'todos':
            Query = Query.filter(recursos_id=recurso)
        if usuario != 'todos':
            Query = Query.filter( aprobador_id=usuario)
        if estatus != 'todos':
            Query = Query.filter(estatus=estatus)
        if proveedor != 'todos':
            Query = Query.filter(proveedor_id=proveedor)


        Query = Query.order_by( '-pk' )
        ordenes = Query
        #fecha_hoy = str( fecha_i.strftime( "%d-%M-%Y" ) ) + " - " + str( fecha_f.strftime( "%d-%M-%Y" ) )
        return render(
            request,
            'reportes_ordenes/listar_ordenes.html',

                       {''
                        'ordenes': ordenes,
                        'ReporteOrden_form': ReporteOrden_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos,
                        'recursos':recursos,
                        'proveedores': proveedores
                        } )
@login_required
def ReporteCompras(request):
    if request.user.has_perm("personas.view_compra") == False:
        SinPermisos(request)
    ReporteCompra_form = None
    error = None
    compra = Compra()
    departamentos = Departamento.objects.all()
    personas = Usuario.objects.all()
    productos = Producto.objects.all()
    recursos = Recurso.objects.all()

    if request.method == 'GET':
        ReporteCompra_form = ReporteComprasForm( instance=compra )
        compras = Compra.objects.all()
        return render( request,
                       'reportes_compras/listar_compras.html',
                       {#'compras': compras,
                        'ReporteCompra_form': ReporteCompra_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos} )
    else:

        fecha_creacion = request.POST.get( 'fecha_creacion',None)


        descripcion = request.POST.get( 'descripcion' )


        Query = Compra.objects.filter(descripcion__contains=descripcion)
        producto = request.POST.get( 'producto_id' )
        usuario = request.POST.get( 'aprobador_id' )
        estatus = request.POST.get( 'estatus' )


        if request.POST.get( 'departamento_id' ) != 'todos':
            dep = Departamento.objects.get( id=request.POST.get( 'departamento_id' ) )
            req = None
            req = Requisicion.objects.filter( departamento_id=dep.id )
            ord = OrdenCompra.objects.filter(requerimiento_id__in=req)
            Query = Query.filter(ordenCompra_id__in=ord)

        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter( fecha_creacion__range=[fecha_i, fecha_f])
        #if departamento != 'todos':
        #    Query = Query.filter( ordenCompra_id.requerimiento_id.departamento_id=departamento)
        if usuario != 'todos':
            Query = Query.filter( aprobador_id=usuario)
        if estatus != 'todos':
            Query = Query.filter(estatus=estatus)

        Query = Query.order_by( '-pk' )
        compras = Query
        return render(
            request,
            'reportes_compras/listar_compras.html',

                       {''
                        'compras': compras,
                        'ReporteCompra_form': ReporteCompra_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos
                        } )

@login_required
def ReporteVehiculos(request):
    if request.user.has_perm("personas.view_ordencompra") == False:
        SinPermisos(request)
    ReporteOrden_form = None
    error = None
    orden = OrdenCompra()
    departamentos = Departamento.objects.all()
    personas = Usuario.objects.all()
    productos = Producto.objects.filter(id__in=[3,5,13,19,21])
    recursos = Recurso.objects.all()
    vehiculos = Vehiculo.objects.all()

    if request.method == 'GET':
        ReporteOrden_form = ReporteOrdenesForm( instance=orden )
        ordenes = OrdenCompra.objects.all()
        return render( request,
                       'reportes_vehiculos/listar_ordenes.html',
                       {
                        'ReporteOrden_form': ReporteOrden_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos,
                        'recursos':recursos,
                        'vehiculos':vehiculos} )
    else:

        fecha_creacion = request.POST.get( 'fecha_creacion',None)
        descripcion = request.POST.get( 'descripcion' )

        Query = OrdenCompra.objects.filter(descripcion__contains=descripcion)
        recurso = request.POST.get( 'recurso_id' )
        usuario = request.POST.get( 'aprobador_id' )



        estatus = request.POST.get( 'estatus' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter(fecha_creacion__range=[fecha_i, fecha_f] )

        if request.POST.get( 'producto_id' ) != 'todos':
            producto = Producto.objects.filter( id=request.POST.get( 'producto_id' ) )
            req = None
            req = Requisicion.objects.filter(producto_id__in=producto)
            Query = Query.filter( requerimiento_id__in=req )
        else:
            req = None
            req = Requisicion.objects.filter( producto_id__in=productos )
            Query = Query.filter( requerimiento_id__in=req )

        if request.POST.get( 'departamento_id' ) != 'todos':
            dep = Departamento.objects.get( id=request.POST.get( 'departamento_id' ) )
            req = None
            req = Requisicion.objects.filter( departamento_id=dep.id )
            Query = Query.filter(requerimiento_id__in=req)

        if request.POST.get( 'vehiculo_id' ) != 'todos':
            vehiculo = Vehiculo.objects.get( id=request.POST.get( 'vehiculo_id' ) )
            req = None
            req = Requisicion.objects.filter( vehiculo_id=vehiculo.id )
            Query = Query.filter(requerimiento_id__in=req)

        #req = Requisicion.objects.filter(vehiculo_id>0)
        #Query = Query.filter( requerimiento_id__in=req )

        if recurso != 'todos':
            Query = Query.filter(recursos_id=recurso)
        if usuario != 'todos':
            Query = Query.filter( aprobador_id=usuario)
        if estatus != 'todos':
            Query = Query.filter(estatus=estatus)

        Query = Query.order_by( '-pk' )
        ordenes = Query
        return render(
            request,
            'reportes_vehiculos/listar_ordenes.html',

                       {''
                        'ordenes': ordenes,
                        'ReporteOrden_form': ReporteOrden_form,
                        'personas':personas,
                        'departamentos':departamentos,
                        'productos': productos,
                        'recursos':recursos,
                        'vehiculos':vehiculos
                        })

@login_required
def ListarBitacora(request):
    if request.user.has_perm("personas.view_bitacora") == False:
        SinPermisos(request)

    if request.method == 'POST':
        fecha_creacion = request.POST.get( 'fecha_creacion', None )
        if len( fecha_creacion ) > 2:
            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            bitacoras = Bitacora.objects.filter(fecha_creacion__range=[fecha_i, fecha_f])
            #Query = Bitacora.filter( fecha_creacion__range=[fecha_i, fecha_f] )
            #bitacoras = Query
            return render( request, 'bitacora/listar_bitacora.html', {'bitacoras': bitacoras} )
    #SI NO SE MANDAN TODAS LA BITACORAS
    bitacoras = Bitacora.objects.all()
    return render( request, 'bitacora/listar_bitacora.html', {'bitacoras': bitacoras} )

##CREACION DE FUNCIONES PARA CONCEPTO#DEFINICION DE FUNCIONES PARA LOS RECURSOS
def CrearConcepto(request):
    if request.user.has_perm("personas.add_concepto") == False:
        SinPermisos(request)
    if request.method == 'POST':
        concepto_form = ConceptoForm(request.POST)
        if concepto_form.is_valid():
            concepto_form.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Concepto agregado correctamente: " + concepto_form.cleaned_data['nombre'] )
            return redirect('listar_conceptos')
    else:
        concepto_form = ConceptoForm()
    return render(request, 'conceptos/crear_concepto.html',{'concepto_form': concepto_form})
@login_required
def ListarConceptos(request):
    if request.user.has_perm("personas.view_concepto") == False:
        SinPermisos(request)
    conceptos = Concepto.objects.all()
    return render(request, 'conceptos/listar_conceptos.html', {'conceptos':conceptos })
@login_required
def EditarConcepto(request, id):
    if request.user.has_perm("personas.change_concepto") == False:
        SinPermisos(request)
    concepto_form = None
    error = None
    try:
        concepto = Concepto.objects.get( id=id)

        if request.method == 'GET':
            concepto_form = ConceptoForm( instance=concepto )
        else:
            concepto_form = ConceptoForm( request.POST, instance=concepto )
            if concepto_form.is_valid():
                concepto_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Concepto editado correctamente: " + concepto_form.cleaned_data['nombre'] )
            return redirect( 'listar_conceptos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'conceptos/crear_concepto.html', {'concepto_form': concepto_form,'error':error})
@login_required
def EliminarConcepto(request,id):
    if request.user.has_perm("personas.delete_concepto") == False:
        SinPermisos(request)
    concepto = Concepto.objects.get(id=id)
    if request.method == 'POST':
        concepto.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Concepto eliminado correctamente: " + concepto.nombre )
        return redirect('listar_conceptos')
    return render(request,'conceptos/eliminar_concepto.html', {'concepto':concepto})

##CREACION DE FUNCIONES PARA LAS VENTAS
@method_decorator(csrf_exempt)
def CrearVenta(request):
    if request.user.has_perm("personas.add_venta") == False:
        SinPermisos(request)
    data = {}
    if request.method == 'POST': #and request.POST['action']=='autocomplete' :
        data = {}

        try:
            action = request.POST['action']

            if action == 'autocomplete':
                data = []
                for i in Concepto.objects.filter( Q(nombre__icontains=request.POST['term']) | Q(clave__icontains=request.POST['term']) )[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    item['pvp'] = float(i.precio)

                    data.append( item )
            elif action == 'add':
                with transaction.atomic():   # con transaction atomic si llega a surgir un error al agregar prods se hace rollback
                    vents = json.loads(request.POST['vents'])
                    print(vents)
                    venta = Venta()
                    venta.cliente = vents['cliente']
                    venta.monto = vents['subtotal']
                    venta.fecha_creacion = datetime.now()
                    venta.save()
                    for i in vents['products']:
                        conceptoVta = ConceptoVenta()
                        conceptoVta.venta_id = venta
                        conceptoVta.concepto_id = Concepto.objects.get(id=i['id'])
                        conceptoVta.cantidad = i['cant']
                        conceptoVta.precio_unitario = i['precio']
                        conceptoVta.subtotal = i['subtotal']
                        conceptoVta.save()

            else:

                data['error'] = 'Ha ocurrido un error'

        except Exception as e:
            data['error'] = str(e)
            print(data['error'])


        return JsonResponse( data, safe=False )

    else:
        venta_form = VentaForm()
        conceptos = ConceptosForm()
        fecha = datetime.now().strftime("%d-%m-%Y")
    return render(request, 'ventas/crear_venta.html',{'venta_form': venta_form,'conceptos':conceptos, 'fecha':fecha})
@login_required
def ListarVentas(request):
    if request.user.has_perm("personas.view_venta") == False:
        SinPermisos(request)
    ventas = Venta.objects.filter(visible='si').order_by( '-pk' )
    detalles = ConceptoVenta.objects.filter(venta_id__in=ventas)

    return render(request, 'ventas/listar_ventas.html', {'ventas':ventas,'detalles':detalles })
@login_required
def EditarVenta(request, id):
    if request.user.has_perm("personas.change_venta") == False:
        SinPermisos(request)
    venta_form = None
    error = None
    try:
        venta = Venta.objects.get( id=id)

        if request.method == 'GET':
            venta_form = VentaForm( instance=venta )
        else:
            venta_form = VentaForm( request.POST, instance=venta )
            if venta_form.is_valid():
                venta_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Venta editada correctamente: " + venta_form.cleaned_data['id'] )
            return redirect( 'listar_ventas' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'ventas/crear_venta.html', {'venta_form': venta_form,'error':error})
@login_required
def EliminarVenta(request,id):
    if request.user.has_perm("personas.delete_venta") == False:
        SinPermisos(request)
    venta = Venta.objects.get(id=id)
    if request.method == 'POST':
        venta.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Se ha eliminado correctamente la venta " )
        return redirect('listar_ventas')
    return render(request,'ventas/eliminar_venta.html', {'venta':venta})
#ESTA FUNCION CAMBIA EL ESTATUS DE LA FUNCION PARA NO PODER SER ELIMINADA EN EL LISTADO
@login_required
def TerminarVenta(request,id):
    venta = Venta.objects.get(id=id)
    venta.visible = 'no'
    venta.save()
    return redirect( 'listar_ventas' )
#CODIGO PARA MANDAR IMPRIMIR LA REQUISICION
def ImprimirVenta(request,id):
    if request.user.has_perm("personas.view_venta") == False:
        SinPermisos(request)
    venta = None
    fecha = datetime.now()
    venta = Venta.objects.get(id=id)
    detalles = ConceptoVenta.objects.filter(venta_id = venta)
    return render(request, 'ventas/imprimir_venta.html', {'venta': venta,'detalles':detalles,'fecha':fecha} )
#REPORTE DE VENTAS
@login_required
def ReporteVentas(request):
    if request.user.has_perm( "personas.view_venta" ) == False:
        SinPermisos( request )

    ReporteVenta_form = None
    error = None
    ventas = Venta()
    conceptos = Concepto.objects.all()       # campos para busqueda por concepto de vta
    if request.method == 'GET':

        ventas = Venta.objects.all()
        return render( request,
                       'reportes_ventas/listar_ventas2.html',
                       { 'conceptos': conceptos}
                     )
    else:

        Query = Venta.objects.filter( cliente__contains=request.POST.get( 'cliente' ))
        fecha_creacion = request.POST.get( 'fecha_creacion' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter( fecha_creacion__range=[fecha_i, fecha_f] )

        if request.POST.get( 'concepto_id' ) != 'todos':
            Query = Query.filter( concepto_id=request.POST.get( 'concepto_id' ) )

        Query = Query.order_by('-pk')
        ventas = Query
        detalles = ConceptoVenta.objects.all()
        return render(
            request,
            'reportes_ventas/listar_ventas2.html',

                       {''
                        'ventas': ventas,
                        'ReporteVenta_form': ReporteVenta_form,
                        'conceptos': conceptos,
                        'detalles': detalles
                        } )
##CREACION DE FUNCIONES PARA LOS TIPOS DE VEHICULOS
def CrearTiposVehiculo(request):
    if request.user.has_perm("personas.add_tiposvehiculo") == False:
        SinPermisos(request)
    if request.method == 'POST':
        tiposvehiculo_form = TiposVehiculoForm(request.POST)
        if tiposvehiculo_form.is_valid():
            tiposvehiculo_form.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Tipo agregado correctamente: " + tiposvehiculo_form.cleaned_data['nombre'] )
            return redirect('listar_tiposvehiculos')
    else:
        tiposvehiculo_form = TiposVehiculoForm()
    return render(request, 'tiposvehiculo/crear_tiposvehiculo.html',{'tiposvehiculo_form': tiposvehiculo_form})
@login_required
def ListarTiposVehiculos(request):
    if request.user.has_perm("personas.view_tiposvehiculo") == False:
        SinPermisos(request)
    tiposvehiculos = TiposVehiculo.objects.all()
    return render(request, 'tiposvehiculo/listar_tiposvehiculos.html', {'tiposvehiculos':tiposvehiculos })
@login_required
def EditarTiposVehiculo(request, id):
    if request.user.has_perm("personas.change_tiposvehiculo") == False:
        SinPermisos(request)
    tiposvehiculo_form = None
    error = None
    try:
        tiposvehiculo = TiposVehiculo.objects.get( id=id)

        if request.method == 'GET':
            tiposvehiculo_form = TiposVehiculoForm( instance=tiposvehiculo )
        else:
            tiposvehiculo_form = TiposVehiculoForm( request.POST, instance=tiposvehiculo )
            if tiposvehiculo_form.is_valid():
                tiposvehiculo_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Tipo editado correctamente: " + tiposvehiculo_form.cleaned_data['nombre'] )
            return redirect( 'listar_tiposvehiculos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'tiposvehiculo/crear_tiposvehiculo.html', {'tiposvehiculo_form': tiposvehiculo_form,'error':error})
@login_required
def EliminarTiposVehiculo(request,id):
    if request.user.has_perm("personas.delete_tiposvehiculo") == False:
        SinPermisos(request)
    tiposvehiculo = TiposVehiculo.objects.get(id=id)
    if request.method == 'POST':
        tiposvehiculo.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Tipo de vehiculo eliminado correctamente: " + tiposvehiculo.nombre )
        return redirect('listar_tiposvehiculos')
    return render(request,'tiposvehiculo/eliminar_tiposvehiculo.html', {'tiposvehiculo':tiposvehiculo})

#FUNCIONES PARA ADMINISTRAR LOS VEHICULOS
@login_required
def CrearVehiculo(request):
    if request.user.has_perm("personas.add_vehiculo") == False:
        SinPermisos(request)
    if request.method == 'POST':
        vehiculo_form = VehiculoForm(request.POST)
        if vehiculo_form.is_valid():
            vehiculo_form.save()
            bitacora = Bitacora(fecha_creacion=datetime.now(),folio = str(vehiculo_form.cleaned_data['nombre']) +"("+ str(vehiculo_form.cleaned_data['departamento_id']) + ")",estatus="Auto Agregado",usuario=request.user.nombres,tipo_documento="inventario vehiculo")
            bitacora.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Auto agregado correctamente: " + vehiculo_form.cleaned_data['nombre'] )
            return redirect('listar_vehiculos')
    else:
        vehiculo_form = VehiculoForm()
    return render(request, 'vehiculos/crear_vehiculo.html',{'vehiculo_form': vehiculo_form})
@login_required
def ListarVehiculo(request):
    if request.user.has_perm("personas.view_vehiculo") == False:
        SinPermisos(request)
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/listar_vehiculos.html', {'vehiculos':vehiculos})
@login_required
def EditarVehiculo(request, id):
    if request.user.has_perm("personas.change_vehiculo") == False:
        SinPermisos(request)
    vehiculo_form = None
    error = None
    try:
        vehiculo = Vehiculo.objects.get(id=id)

        if request.method == 'GET':
            vehiculo_form = VehiculoForm( instance=vehiculo )
        else:
            vehiculo_form = VehiculoForm( request.POST, instance=vehiculo )
            if vehiculo_form.is_valid():
                vehiculo_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Auto editado correctamente: " + vehiculo_form.cleaned_data[
                                          'nombre'] )
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( vehiculo_form.cleaned_data['nombre'] ) + "(" + str(
                                         vehiculo_form.cleaned_data['departamento_id'] ) + ")",
                                     estatus="Vehiculo Editado",
                                     usuario=request.user.nombres,
                                     tipo_documento="inventario vehiculo" )
                bitacora.save()
            return redirect( 'listar_vehiculos' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'vehiculos/crear_vehiculo.html', {'vehiculo_form': vehiculo_form,'error':error})
@login_required
def EliminarVehiculo(request,id):
    if request.user.has_perm("personas.delete_vehiculo") == False:
        SinPermisos(request)
    vehiculo = Vehiculo.objects.get(id=id)
    if request.method == 'POST':
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( vehiculo.nombre ) + "(" + str(
                                 vehiculo.departamento_id ) + ")",
                             estatus="Vehiculo Eliminado",
                             usuario=request.user.nombres, tipo_documento="inventario vehiculo" )
        bitacora.save()
        vehiculo.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="vehiculo eliminado correctamente: " + vehiculo.nombre )
        return redirect('listar_vehiculos')
    return render(request, 'vehiculos/eliminar_vehiculo.html', {'vehiculo':vehiculo})

