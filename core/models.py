from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    correo = models.CharField(unique=True, max_length=100)
    contraseña_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=13)
    fecha_registro = models.DateTimeField()
    activo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    id_mascota = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    especie = models.CharField(max_length=45)
    raza = models.CharField(max_length=45)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=6)
    estado_salud = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.FileField(upload_to='img/', max_length=255, blank=True, null=True)
    estado_adopcion = models.CharField(max_length=10)
    fecha_ingreso = models.DateField()

    class Meta:
        managed = False
        db_table = 'mascota'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=45)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.FileField(upload_to='img/', max_length=255, blank=True, null=True)
    disponibilidad = models.IntegerField()
    usuario_id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='usuario_id_usuario')

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return self.nombre


class ArticuloInformativo(models.Model):
    codigo_articulo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    contenido = models.TextField()
    fecha_publicacion = models.DateField()
    categoria = models.CharField(max_length=45)
    imagen = models.FileField(upload_to='img/', max_length=255, blank=True, null=True)
    usuario_id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='usuario_id_usuario')

    class Meta:
        managed = False
        db_table = 'articulo_informativo'

    def __str__(self):
        return self.titulo


class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField()
    estado = models.CharField(max_length=7)
    usuario_id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='usuario_id_usuario')

    class Meta:
        managed = False
        db_table = 'carrito'

    def __str__(self):
        return f"Carrito {self.id_carrito}"


class DetalleCarrito(models.Model):
    id_carrito = models.OneToOneField(Carrito, models.CASCADE, db_column='id_carrito', primary_key=True)
    id_producto = models.ForeignKey(Producto, models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalle_carrito'
        unique_together = (('id_carrito', 'id_producto'),)


class SolicitudAdopcion(models.Model):
    id_adopcion = models.AutoField(primary_key=True)
    fecha_solicitud = models.DateField()
    estado = models.CharField(max_length=9)
    notas = models.TextField(blank=True, null=True)
    usuario_id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='usuario_id_usuario')
    mascota_id_mascota = models.ForeignKey(Mascota, models.CASCADE, db_column='mascota_id_mascota')

    class Meta:
        managed = False
        db_table = 'solicitud_adopcion'

    def __str__(self):
        return f"Adopcion {self.id_adopcion}"