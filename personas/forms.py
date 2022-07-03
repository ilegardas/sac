from django import forms
from .models import Departamento, Recurso, Producto, Proveedor, Inventario, Requisicion, Usuario, OrdenCompra, Compra, \
    Concepto, Venta, Vehiculo, TiposVehiculo


class UploadFileForm(forms.Form):

    Logotipo = forms.FileField()

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion']
        labels={
            'nombre': 'Nombre del Departamento',
            'Descripcion': 'Descripcion del Departamento'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs ={
                    'class':'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password','email','nombres','apellidos','departamento_id','imagen','telefono','is_active','is_staff']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'departamento_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )

        }


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','categoria', 'descripcion']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'categoria': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre','descripcion', 'telefono','email','direccion','rfc']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'rfc': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )

        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto_id','categoria','unidad_medida', 'descripcion','stock','stock_min']
        widgets = {
            'categoria': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'unidad_medida': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'stock': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'stock_min': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'producto_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }

class RequisicionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super( RequisicionForm, self ).__init__( *args, **kwargs )
        self.fields['proveedor_id'].empty_label = None
        self.fields['recursos_id'].queryset = Recurso.objects.filter( visible='si' )

    class Meta:
        model = Requisicion
        fields = ['departamento_id','persona_id', 'recursos_id','producto_id','proveedor_id','descripcion','vehiculo_id']
        widgets = {
            'departamento_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'disabled': True


                }

            ),
            'persona_id': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'readonly': True,
                    'disabled': True



                }

            ),
            'recursos_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',
                    'readonly': False,
                    'disabled': False

                }

            ),
            'proveedor_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',
                    'readonly': False,
                    'disabled': False,
                    'blank': False

                }

            ),
            'producto_id': forms.SelectMultiple(
                attrs={
                    'class': 'form-control form-control-user',

                }

            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'vehiculo_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',

                }

            )

        }
class OrdenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super( OrdenForm, self ).__init__( *args, **kwargs )
        self.fields['proveedor_id'].empty_label = None

    class Meta:
        model = OrdenCompra

        fields = ['recursos_id','proveedor_id', 'descripcion','cantidad_prod','precio_unitario','precio_total']
        widgets = {
            'recursos_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',

                }

            ),
            'proveedor_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',
                },
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-user'
                }
            ),
            'cantidad_prod': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'precio_unitario': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'precio_total': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )

}

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['descripcion','pdf', 'xml','Total','estatus']
        widgets = {
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'readonly': False,
                    'disabled': False


                }

            ),
            'pdf': forms.FileInput(


            ),
            'xml': forms.FileInput(

            ),
            'Total': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'estatus': forms.Select(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
}
class ReporteRequisicionesForm(forms.ModelForm):
    class Meta:

        model = Requisicion
        fields = ['fecha_creacion']
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control'

                }
           )
        }
class ReporteOrdenesForm(forms.ModelForm):
    class Meta:

        model = OrdenCompra
        fields = ['fecha_creacion']
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control'

                }
           )
        }
class ReporteComprasForm(forms.ModelForm):
    class Meta:

        model = Compra
        fields = ['fecha_creacion']
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control'

                }
           )
        }
class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['nombre', 'clave','precio']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'clave': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'precio': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }
class VentaForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['cliente'].widget.attrs['autofocus']=True
        self.fields['cliente'].widget.attrs['required'] = False
        self.fields['cliente'].widget.attrs['class'] = 'form-control select2'
        self.fields['monto'].widget.attrs['readonly'] = 'True'
        self.fields['monto'].widget.attrs['default'] = '0.0'
    class Meta:
        model = Venta
        fields = ['monto','cliente']
        widgets = {
            'monto': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'cliente': forms.TextInput(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'required':'False',
                    'blank':'True'

                }
            )
        }
class TiposVehiculoForm(forms.ModelForm):
    class Meta:
        model = TiposVehiculo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )
        }
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        CHOICES = (('Carro', 'Carro'), ('Camioneta', 'Camioneta'),('Troca', 'Troca'),('Motocicleta', 'Motocicleta'),('Maquinaria', 'Maquinaria'),)
        tipo = forms.ChoiceField( choices=CHOICES )
        #SINO = (('si', 'si'), ('no', 'no'),)
        #visible = forms.ChoiceField( choices=SINO )
        fields = ['nombre','num_economico','marca','submarca','modelo', 'tipo','placas','color','visible','departamento_id','fecha_mantenimiento','anotaciones']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'num_economico': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'submarca': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'placas': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'tipo': forms.Select(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'departamento_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
            'visible': forms.Select(choices=(('no', 'No'), ('si', 'Si')),
                                    attrs={
                                        'class': 'form-control form-control-user'

                                    }

            ),
            'fecha_mantenimiento': forms.SelectDateWidget(

           ),
            'anotaciones': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-user'

                }

            ),
        }
class ProductosForm(forms.Form):
    productos = forms.ModelChoiceField(queryset=Producto.objects.all() , widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    vehiculos = forms.ModelChoiceField(queryset=Vehiculo.objects.filter(visible='si'), required=False ,blank=True, widget=forms.Select(attrs={
        'class': 'form-control',
        'blank':'True',
        'null':'True',
        'initial':'vacio'

    }))
#Para obtener selec de conceptos
class ConceptosForm(forms.Form):
    concepto = forms.ModelChoiceField( queryset=Concepto.objects.all(), required=False ,blank=True, widget=forms.Select( attrs={
        'class': 'form-control select2'
    } ) )
class ReporteFechasForm(forms.Form):
    class Meta:

        model = Requisicion
        fields = ['fecha_creacion']
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control'

                }
           )
        }