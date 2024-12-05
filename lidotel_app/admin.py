from django.contrib import admin
from .models import Agencia, ConfiguracionPuntos, TipoHabitacion, Reserva

@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre_agencia', 'usuario', 'puntos_actuales')
    search_fields = ('nombre_agencia', 'usuario__username')

@admin.register(ConfiguracionPuntos)
class ConfiguracionPuntosAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Puntos Base', {
            'fields': ('puntos_habitacion_estandar', 'puntos_suite', 'puntos_grupo')
        }),
        ('Puntos por Estadía', {
            'fields': ('puntos_estadia_corta', 'puntos_estadia_media', 'puntos_estadia_larga')
        }),
        ('Servicios Adicionales', {
            'fields': ('puntos_transporte', 'puntos_tours', 'puntos_spa')
        }),
        ('Multiplicadores', {
            'fields': ('multiplicador_temporada_alta', 'multiplicador_ultimo_minuto')
        }),
        ('Programa de Fidelización', {
            'fields': ('bonus_fidelizacion', 'huespedes_para_bonus')
        }),
    )

@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos_base')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_huesped', 'agencia', 'tipo_habitacion', 'fecha_checkin', 'fecha_checkout', 'estado', 'puntos_generados')
    list_filter = ('estado', 'tipo_habitacion', 'agencia')
    search_fields = ('nombre_huesped', 'numero_documento')
    readonly_fields = ('puntos_generados',)
    fieldsets = (
        ('Información del Huésped', {
            'fields': ('nombre_huesped', 'numero_documento', 'telefono', 'email')
        }),
        ('Detalles de la Reserva', {
            'fields': ('agencia', 'tipo_habitacion', 'fecha_checkin', 'fecha_checkout', 
                      'numero_habitaciones', 'numero_huespedes')
        }),
        ('Preferencias', {
            'fields': ('no_fumador', 'vista_mar', 'acceso_discapacitados', 'cama_adicional')
        }),
        ('Servicios Adicionales', {
            'fields': ('transporte_aeropuerto', 'tours_locales', 'servicio_spa')
        }),
        ('Estado y Puntos', {
            'fields': ('estado', 'puntos_generados', 'comentarios')
        }),
    )
