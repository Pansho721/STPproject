from django.db import models  # Importación del módulo de modelos de Django
from Clases import Admin, Cliente, Pedido, Plato

# Modelo que representa a un cliente y su pedido
class Cliente(models.Model):
    nro_pedido = models.IntegerField()  # Número del pedido asociado al cliente
    pedido = models.TextField(blank=True)  # Descripción del pedido (puede estar vacío)
    nro_mesa = models.IntegerField()  # Número de mesa del cliente

    def __str__(self):
        # Representación en cadena del objeto, útil para panel de administración
        return f"Pedido #{self.nro_pedido}"

# Modelo que representa un plato del menú
class Plato(models.Model):
    name = models.CharField(max_length=150)  # Nombre del plato
    list_ingredientes = models.CharField(max_length=150)  # Lista de ingredientes como texto plano
    categoria = models.CharField(max_length=50)  # Categoría del plato
    precio = models.IntegerField()  # Precio del plato
    promedio_puntuacion = models.FloatField(default=0)  # Promedio de las puntuaciones de los comentarios

# Modelo que representa a un administrador del sistema
class Admin(models.Model):
    name = models.CharField(max_length=50)  # Nombre del administrador
    password = models.CharField(max_length=50)  # Contraseña (nota: no está cifrada, esto es inseguro en producción)

# Modelo que representa un comentario sobre un plato
class Comentario(models.Model):
    plato = models.ForeignKey(
        Plato,
        on_delete=models.CASCADE,  # Si se elimina el plato, también se eliminan los comentarios asociados
        related_name='comentarios'  # Permite acceder a comentarios desde un plato: plato.comentarios.all()
    )
    texto = models.CharField(max_length=300)  # Texto del comentario
    puntuacion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # Puntuación del 1 al 5

# Modelo que representa un pedido realizado por un cliente
class Pedido(models.Model):
    id = models.BigAutoField(primary_key=True)  # ID único del pedido
    platos = models.ManyToManyField(Plato, related_name='pedidos')  # Lista de platos
    numero_mesa = models.IntegerField()  # Número de mesa donde se realizó el pedido
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación automática al guardar
    servido = models.BooleanField(default=False)  # Indica si el pedido fue servido o no