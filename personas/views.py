
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from personas.forms import DepartamentoForm, RecursoForm, ProductoForm, ProveedorForm, InventarioForm, RequisicionForm, OrdenForm, CompraForm, UsuarioForm, ReporteRequisicionesForm, ReporteOrdenesForm, ReporteComprasForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from personas.models import Departamento, Recurso, Producto, Proveedor, Inventario, Requisicion, OrdenCompra, Compra, Usuario, Bitacora
from django.contrib.auth import logout
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.


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
        departamento_id = departamento
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

        usuario.save()
        messages.add_message( request=request, level=messages.SUCCESS, message="Usuario Creado Exitósamente" )
        my_group = Group.objects.get( name=grupo ) #obtenemos el grupo seleccionado de los permisos
        if my_group is not None: #Nos aseguramos que encuentre un valor
            my_group.user_set.add(usuario) # se agrega el nuevo usuario al grupo
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
        producto = Producto.objects.get(id=request.POST.get('producto_id'))
        departamento = usuario.departamento_id
        persona = request.user
        concepto = request.POST.get('concepto')
        producto_id = request.POST.get('producto_id')
        descripcion = request.POST.get('descripcion')
        fecha_creacion = datetime.now()
        fecha_estatus = datetime.now()
        estatus = 'pendiente'

        requisicion = Requisicion(
            departamento_id=departamento,
            persona_id=persona,
            concepto=concepto,
            producto_id=producto,
            descripcion=descripcion,
            estatus=estatus,
            fecha_creacion = fecha_creacion,
            fecha_estatus = fecha_estatus,

        )

        requisicion.save()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Requerimiento creado correctamente: " + requisicion.descripcion )
        #SE ENVIA CORREO DE NOTIFICACION DE REQUERIMIENTO CREADO HACIA LOS APROBADORES
        aprobadores_mail = []
        aprobadores = Usuario.objects.filter( groups__name__in=['Aprobador'] )
        for aprobador in aprobadores:
            aprobadores_mail.append( aprobador.email )
        mensaje = "Se ha creado un requerimiendo solicitando: " + str(requisicion.descripcion) + ", creado por:" + str(requisicion.persona_id) + " del departamento de: " + str(requisicion.departamento_id)
        Notificar(request,'creacion de requerimiento',mensaje,aprobadores_mail)
        #SE GUARDA A LA BITACORA LA REQUISICION CREADA
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( requisicion.concepto ) + "(" + str(
                                 requisicion.producto_id ) + ")",
                             estatus="Requerimiento Creado",
                             usuario=request.user.nombres,
                             tipo_documento="Requerimiento" )
        bitacora.save()
        #SE REDIRECCIONA A LA LISTA DE REQUERIMIENTOS DEL USUARIO
        return redirect('listar_requisiciones')
    else:
        requisicion_form = RequisicionForm()

    return render(request, 'requisiciones/crear_requisicion.html',{'requisicion_form': requisicion_form,'usuario':usuario})
@login_required
def ListarRequisiciones(request):

    if request.user.has_perm( "personas.view_requisicion" ) == False:
        SinPermisos( request )
    requisiciones = Requisicion.objects.filter(estatus='pendiente',persona_id=request.user)
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
            requisicion_form = RequisicionForm(instance=requisicion)
        else:
            requisicion_form = RequisicionForm(request.POST, instance=requisicion)
            requisicion = Requisicion.objects.get(id=requisicion.id)
            requisicion.concepto = request.POST.get('concepto')
            requisicion.descripcion = request.POST.get('descripcion')
            requisicion.producto_id = Producto.objects.get(id = request.POST.get('producto_id'))
            requisicion.save()
            messages.add_message( request=request, level=messages.SUCCESS,
                                  message="Requerimiento editado correctamente: " + requisicion.descripcion )
            bitacora = Bitacora( fecha_creacion=datetime.now(),
                                 folio=str( requisicion.concepto ) + "(" + str(
                                     requisicion.producto_id ) + ")",
                                 estatus="Requerimiento Editado",
                                 usuario=request.user.nombres,
                                 tipo_documento="Requerimiento" )
            bitacora.save()

            return redirect('listar_requisiciones')
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'requisiciones/crear_requisicion.html', {'requisicion_form': requisicion_form,'error':error,'usuario':usuario})
@login_required
def EliminarRequisicion(request,id):
    if request.user.has_perm("personas.delete_requisicion") == False:
        SinPermisos(request)
    usuario = ObtenUsuario( request )
    requisicion = Requisicion.objects.get(id=id)
    if request.method == 'POST':
        requisicion.delete()
        messages.add_message( request=request, level=messages.SUCCESS,
                              message="Requerimiento eliminado correctamente: " + requisicion.descripcion )
        #Se guarda en la bitacora
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( requisicion.concepto ) + "(" + str(
                                 requisicion.producto_id ) + ")",
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
    messages.add_message( request=request, level=messages.SUCCESS,
                          message="Requerimiento cancelado correctamente: " + requisicion.descripcion )
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( requisicion.concepto ) + "(" + str(
                             requisicion.producto_id ) + ")",
                         estatus="Requerimiento Cancelado",
                         usuario=request.user.nombres,
                         tipo_documento="Requerimiento" )
    bitacora.save()
    return redirect('listar_ordenes')
#ESTA FUNCION CAMBIA EL ESTATUS DE LA FUNCION PARA NO PODER SER ELIMINADA EN EL LISTADO
@login_required
def OrdenDeRequisicion(request,id):
    requisicion = Requisicion.objects.get(id=id)
    requisicion.estatus = 'procesado'
    requisicion.fecha_estatus = datetime.now()
    requisicion.save()
    return ('generado')
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

    if request.method == 'POST':
        requerimiento_id = requisicion
        aprobador_id = usuario
        recursos_id = Recurso.objects.get(id=request.POST.get('recursos_id'))
        proveedor_id = Proveedor.objects.get(id=request.POST.get('proveedor_id'))
        producto_id = requisicion.producto_id
        descripcion = request.POST.get('descripcion')
        estatus = 'pendiente'
        cantidad = request.POST.get('cantidad_prod')
        precio_unitario = request.POST.get('precio_unitario')
        precio_total = request.POST.get('precio_total')

        orden = OrdenCompra(
            requerimiento_id=requerimiento_id,
            aprobador_id=aprobador_id,
            recursos_id=recursos_id,
            proveedor_id=proveedor_id,
            producto_id=producto_id,
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
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( orden.proveedor_id ) + "(" + str(
                                 orden.producto_id ) +" " + str(
                                 orden.cantidad_prod ) + ")",
                             estatus="Orden Creada",
                             usuario=request.user.nombres,
                             tipo_documento="Orden de Compra" )
        bitacora.save()
        #SE NOTIFICA A LOS REQUISITORES POR CORREO
        destinatario = (requisicion.persona_id.email,)
        mensaje = "Se ha aprobado su solicitud de compra con descrpcion: " + str( requisicion.descripcion ) + " y concepto: " + str( requisicion.concepto )
        Notificar( request, 'Aprobacion de requerimiento', mensaje, destinatario )
        return redirect('listar_ordenes')
    else:
        orden_form = OrdenForm()

    return render(request, 'ordenes/crear_orden.html',{'orden_form': orden_form,'usuario':usuario,'requisicion':requisicion})

@login_required
def ListarOrdenes(request):
    if request.user.has_perm("personas.view_ordencompra") == False:
        SinPermisos(request)
    requisiciones_l = None
    ordenes_l = None
    requisiciones_l = Requisicion.objects.filter( estatus='pendiente', persona_id=request.user )
    ordenes_l = OrdenCompra.objects.filter( aprobador_id=request.user, estatus='pendiente' )

    return render(request, 'ordenes/listar_ordenes.html', {'requisiciones':requisiciones_l,'ordenes': ordenes_l})
@login_required
def EditarOrden(request, id):
    if request.user.has_perm("personas.change_ordencompra") == False:
        SinPermisos(request)
    orden_form = None
    error = None
    try:
        orden = OrdenCompra.objects.get( id=id)
        requisicion = Requisicion.objects.get(id=orden.requerimiento_id.id)

        if request.method == 'GET':
            orden_form = OrdenForm( instance=orden )
        else:
            orden_form = OrdenForm( request.POST, instance=orden )
            if orden_form.is_valid():
                orden_form.save()
                messages.add_message( request=request, level=messages.SUCCESS,
                                      message="Orden editada correctamente: " + orden_form.cleaned_data['descripcion'] )
                #SE AGREGA EL MOVIMIENTO A LA BITACORA
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( orden_form.cleaned_data['proveedor_id'] ) + "(" + str(
                                         requisicion.producto_id ) + str(
                                         orden_form.cleaned_data['cantidad_prod'] ) + ")",
                                     estatus="Orden Editada",
                                     usuario=request.user.nombres,
                                     tipo_documento="Orden de Compra" )
                bitacora.save()
            return redirect( 'listar_ordenes' )
    except ObjectDoesNotExist as e:
        error=e

    return render(request, 'ordenes/crear_orden.html', {'orden_form': orden_form,'error':error,'requisicion':requisicion})
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
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( orden.proveedor_id ) + "(" + str(
                                 orden.producto_id ) + str(
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
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( orden.proveedor_id ) + "(" + str(
                             orden.producto_id ) + str(
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
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                 compra.ordenCompra_id.producto_id ) + str(
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
    ordenes = OrdenCompra.objects.filter(Q(estatus = 'pendiente'))
    compras = Compra.objects.filter(Q(estatus = 'pendiente') | Q(estatus='pagado'))
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
                bitacora = Bitacora( fecha_creacion=datetime.now(),
                                     folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                         compra.ordenCompra_id.producto_id ) + str(
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
        bitacora = Bitacora( fecha_creacion=datetime.now(),
                             folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                                 compra.ordenCompra_id.producto_id ) + str(
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
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                             compra.ordenCompra_id.producto_id ) + str(
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
    bitacora = Bitacora( fecha_creacion=datetime.now(),
                         folio=str( compra.ordenCompra_id.proveedor_id ) + "(" + str(
                             compra.ordenCompra_id.producto_id ) + str(
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

        fecha_creacion = request.POST.get( 'fecha_creacion' )

        descripcion = request.POST.get( 'descripcion' )

        Query = Requisicion.objects.filter( descripcion__contains=descripcion)
        producto = request.POST.get( 'producto_id' )

        usuario = request.POST.get( 'persona_id' )
        estatus = request.POST.get( 'estatus' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter( fecha_creacion__range=[fecha_i, fecha_f] )

        if producto != 'todos':
            Query = Query.filter(producto_id=producto)

        if usuario != 'todos':
            Query = Query.filter( producto_id=usuario)
        if estatus != 'todos':
            Query = Query.filter(estatus=estatus)


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
                        'recursos':recursos} )
    else:

        fecha_creacion = request.POST.get( 'fecha_creacion',None)
        descripcion = request.POST.get( 'descripcion' )


        Query = OrdenCompra.objects.filter(descripcion__contains=descripcion)
        producto = request.POST.get( 'producto_id' )
        recursos = request.POST.get( 'recurso_id' )
        usuario = request.POST.get( 'aprobador_id' )
        estatus = request.POST.get( 'estatus' )
        if len(fecha_creacion) > 2:

            fechas = fecha_creacion.split( ' ' )
            fecha_i = datetime.strptime( fechas[0], '%d-%m-%Y' )
            fecha_f = datetime.strptime( fechas[2], '%d-%m-%Y' )
            Query = Query.filter(fecha_creacion__range=[fecha_i, fecha_f] )
        if producto != 'todos':
            Query = Query.filter(producto_id=producto)
        if recursos != 'todos':
            Query = Query.filter(recursos_id=recursos)
        if usuario != 'todos':
            Query = Query.filter( aprobador_id=usuario)
        if estatus != 'todos':
            Query = Query.filter(estatus=estatus)


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
                        'recursos':recursos
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
        departamento = request.POST.get( 'departamento_id' )
        # if departamento != 'todos':
        #    Query = Query.filter(producto_id=producto)
        #if producto != 'todos':
        #    Query = Query.filter(producto_id=producto)
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
def ListarBitacora(request):
    if request.user.has_perm("personas.view_bitacora") == False:
        SinPermisos(request)
    bitacoras = Bitacora.objects.all()
    return render(request, 'bitacora/listar_bitacora.html', {'bitacoras':bitacoras})