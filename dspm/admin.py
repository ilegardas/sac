from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Permission
from django.contrib import admin

# Register your models here.
from dspm.models import Incidencia

class IncidenciaResource(resources.ModelResource):
    class Meta:
        model = Incidencia

class   IncidenciaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nombre', 'motivo','fecha_remision','salida','agentes','lugar')
    resource_class = IncidenciaResource

admin.site.register(Incidencia,IncidenciaAdmin)