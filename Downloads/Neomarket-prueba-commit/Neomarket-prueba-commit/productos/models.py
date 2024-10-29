from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    USUARIO_TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('tienda', 'Tienda'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=USUARIO_TIPO_CHOICES)

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo}'


class Producto(models.Model):
    tienda = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'tienda'})
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'cliente'})
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Pago(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, default='pendiente') 

class Pedido(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'cliente'})
    productos = models.ManyToManyField(Producto, through='PedidoProducto')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='pendiente') 

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Venta(models.Model):
    tienda = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'tipo': 'tienda'})
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)