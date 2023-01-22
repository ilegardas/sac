from django.shortcuts import render
@method_decorator(csrf_exempt)
@method_decorator(login_required)
def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)
# Create your views here.


def ObtenUsuario(request):
    current_user = request.user
    usuario = current_user.nombres + " " + current_user.apellidos
    return usuario

def salir(request):
    logout(request)
    messages.add_message(request=request,level=messages.SUCCESS,message="Se ha finalizado la sesion!")
    return redirect('/')

#pantalla para cuando no tengan permisos para determinada pagina
def SinPermisos(request):
    logout(request)
    messages.add_message( request=request, level=messages.SUCCESS, message="No tiene permisos para esta seccion" )
    return render(request, 'sin_permisos/sin_acceso.html')

def CrearIncidencia(request):
    if request.user.has_perm("personas.add_incidencia") == False:
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
