from django import forms
from .models import Incidencia

class UploadFileForm(forms.Form):

    Logotipo = forms.FileField()

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = [
            'nombre',
            'edad',
            'sexo',
            'estado_civil',
            'domicilio',
            'fecha_remision',
            'hora',
            'motivo',
            'evidencia',
            'pertenencias',
            'agentes',
            'lugar',
            'formato_pago',
            'salida',
            'autorizacion_salida',
            'fecha_creacion'
        ]
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