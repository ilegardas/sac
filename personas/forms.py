from django import forms
from .models import Departamento, Recurso, Producto, Proveedor, Inventario, Requisicion, Usuario, OrdenCompra, Compra

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

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
        fields = ['nombre','descripcion', 'telefono','email','rubro','direccion','rfc','contacto']
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
            'rubro': forms.TextInput(
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

            ),
            'contacto': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )

        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['categoria','unidad_medida', 'descripcion','stock','stock_min','producto_id']
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
    class Meta:
        model = Requisicion
        fields = ['departamento_id','persona_id', 'producto_id', 'concepto','descripcion']
        widgets = {
            'departamento_id': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
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
            'producto_id': forms.Select(
                attrs={
                    'class': 'form-control form-control-user',

                }

            ),
            'concepto': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',


                }

            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-user'

                }

            )

        }
class OrdenForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['recursos_id','proveedor_id', 'descripcion','cantidad_prod','precio_unitario','precio_total']
        widgets = {
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
                    'disabled': False



                }

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