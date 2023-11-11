from django.db import models

class Planificacion(models.Model):
    """Este modelo define la entidad Planificación"""
    
    # Entradas
    fecha_actual = models.CharField(max_length=50, null=False, blank=False)
    hora_actual = models.CharField(max_length=20, unique=True, null=False, blank=False)
    usuario = models.CharField(max_length=200, unique=True, null=False, blank=False, default='Sin comentario')
    turno = models.CharField(max_length=20, null=False, blank=False)
    clase_diametrica = models.CharField(max_length=20, null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)
    patron_corte = models.IntegerField(null=False, blank=False)
    productos = models.CharField(max_length=20, null=False, blank=False)
    cantidades = models.CharField(max_length=20, null=False, blank=False)
    rendimiento = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"Planificacion {self.fecha_actual} - {self.hora_actual} - Usuario: {self.usuario} - Turno: {self.turno}"
