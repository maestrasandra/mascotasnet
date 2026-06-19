import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mascotasnet.settings")
django.setup()

from django.utils import timezone
from core.models import Usuario, Producto

created_u = False
u = Usuario.objects.filter(correo='admin').first()
if not u:
    u = Usuario.objects.create(
        nombre='Admin',
        apellido='SuperUser',
        correo='admin',
        contraseña_hash='NA',
        rol='administrador',
        fecha_registro=timezone.now(),
        activo=1
    )
    created_u = True

created_p = False
if Producto.objects.count() == 0:
    Producto.objects.create(nombre='Comida para Perro Adulto 10kg', categoria='Alimentacion', descripcion='Alimento premium.', precio=45000, stock=20, disponibilidad=1, usuario_id_usuario=u)
    Producto.objects.create(nombre='Juguete Hueso Goma', categoria='Juguetes', descripcion='Hueso resistente.', precio=12000, stock=50, disponibilidad=1, usuario_id_usuario=u)
    Producto.objects.create(nombre='Cama Extra Suave', categoria='Accesorios', descripcion='Cama para mascotas.', precio=85000, stock=10, disponibilidad=1, usuario_id_usuario=u)
    created_p = True

print(f'Usuario admin creado: {created_u}. Productos creados: {created_p}')
