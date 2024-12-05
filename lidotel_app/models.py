from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Agencia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_agencia = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    puntos_actuales = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre_agencia

class ConfiguracionPuntos(models.Model):
    # Puntos base por tipo de habitación
    puntos_habitacion_estandar = models.IntegerField(default=10)
    puntos_suite = models.IntegerField(default=15)
    puntos_grupo = models.IntegerField(default=20)
    
    # Puntos por duración de estadía
    puntos_estadia_corta = models.IntegerField(default=5)  # 1-3 noches
    puntos_estadia_media = models.IntegerField(default=10)  # 4-7 noches
    puntos_estadia_larga = models.IntegerField(default=20)  # 8+ noches
    
    # Puntos por servicios adicionales
    puntos_transporte = models.IntegerField(default=5)
    puntos_tours = models.IntegerField(default=5)
    puntos_spa = models.IntegerField(default=10)
    
    # Multiplicadores
    multiplicador_temporada_alta = models.FloatField(default=1.5)
    multiplicador_ultimo_minuto = models.FloatField(default=2.0)
    
    # Bonus por fidelización
    bonus_fidelizacion = models.IntegerField(default=500)  # cada 100 huéspedes
    huespedes_para_bonus = models.IntegerField(default=100)
    
    class Meta:
        verbose_name = "Configuración de Puntos"
        verbose_name_plural = "Configuraciones de Puntos"

class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    puntos_base = models.IntegerField(default=10)
    
    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    
    # Información del huésped
    nombre_huesped = models.CharField(max_length=200)
    numero_documento = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    
    # Detalles de la reserva
    fecha_checkin = models.DateField()
    fecha_checkout = models.DateField()
    numero_habitaciones = models.IntegerField(validators=[MinValueValidator(1)])
    numero_huespedes = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Preferencias
    no_fumador = models.BooleanField(default=False)
    vista_mar = models.BooleanField(default=False)
    acceso_discapacitados = models.BooleanField(default=False)
    cama_adicional = models.BooleanField(default=False)
    
    # Servicios adicionales
    transporte_aeropuerto = models.BooleanField(default=False)
    tours_locales = models.BooleanField(default=False)
    servicio_spa = models.BooleanField(default=False)
    
    # Estado y comentarios
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comentarios = models.TextField(blank=True)
    
    # Puntos generados
    puntos_generados = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def calcular_puntos(self):
        config = ConfiguracionPuntos.objects.first()
        puntos = 0
        
        # Puntos base por tipo de habitación
        if self.tipo_habitacion.nombre.lower() == 'estándar':
            puntos += config.puntos_habitacion_estandar * self.numero_huespedes
        elif self.tipo_habitacion.nombre.lower() == 'suite':
            puntos += config.puntos_suite * self.numero_huespedes
        
        # Puntos por duración de estadía
        duracion = (self.fecha_checkout - self.fecha_checkin).days
        if 1 <= duracion <= 3:
            puntos += config.puntos_estadia_corta * self.numero_huespedes
        elif 4 <= duracion <= 7:
            puntos += config.puntos_estadia_media * self.numero_huespedes
        else:
            puntos += config.puntos_estadia_larga * self.numero_huespedes
        
        # Puntos por servicios adicionales
        if self.transporte_aeropuerto:
            puntos += config.puntos_transporte * self.numero_huespedes
        if self.tours_locales:
            puntos += config.puntos_tours * self.numero_huespedes
        if self.servicio_spa:
            puntos += config.puntos_spa * self.numero_huespedes
        
        # Aplicar multiplicadores si es necesario
        # Aquí puedes agregar la lógica para temporada alta y último minuto
        
        self.puntos_generados = puntos
        return puntos
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva reserva
            self.puntos_generados = self.calcular_puntos()
            self.agencia.puntos_actuales += self.puntos_generados
            self.agencia.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reserva {self.id} - {self.nombre_huesped}"
    
    @property
    def dias_para_editar(self):
        """Retorna el número de días restantes para editar la reserva"""
        dias_transcurridos = (timezone.now() - self.fecha_creacion).days
        return max(30 - dias_transcurridos, 0)
