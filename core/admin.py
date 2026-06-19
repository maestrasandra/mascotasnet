from django.contrib import admin
from .models import Usuario, Mascota, Producto, ArticuloInformativo, Carrito, DetalleCarrito, SolicitudAdopcion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'apellido', 'correo', 'rol', 'activo')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('rol', 'activo')

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id_mascota', 'nombre', 'especie', 'raza', 'estado_adopcion')
    search_fields = ('nombre', 'especie', 'raza')
    list_filter = ('estado_adopcion', 'especie')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'categoria', 'precio', 'stock', 'disponibilidad')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'disponibilidad')

@admin.register(ArticuloInformativo)
class ArticuloInformativoAdmin(admin.ModelAdmin):
    list_display = ('codigo_articulo', 'titulo', 'categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'categoria')
    list_filter = ('categoria',)

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_carrito', 'usuario_id_usuario', 'fecha_creacion', 'estado')
    list_filter = ('estado',)

@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ('id_carrito', 'id_producto', 'cantidad', 'precio_unitario')

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('id_adopcion', 'mascota_id_mascota', 'usuario_id_usuario', 'fecha_solicitud', 'estado')
    list_filter = ('estado',)