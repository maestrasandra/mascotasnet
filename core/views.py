from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from functools import wraps
from .models import Producto, Carrito, DetalleCarrito, Usuario, Mascota, ArticuloInformativo, SolicitudAdopcion
from decimal import Decimal
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# ─── AUXILIARES ──────────────────────────────────────
def get_usuario(request):
    return Usuario.objects.get(correo=request.user.username)

def get_contexto(request):
    contexto = {}
    if request.user.is_authenticated:
        try:
            contexto['usuario'] = Usuario.objects.get(correo=request.user.username)
        except Usuario.DoesNotExist:
            pass
    return contexto

# ─── DECORADORES DE ROL ───────────────────────────────
def cliente_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            usuario = Usuario.objects.get(correo=request.user.username)
            if usuario.rol not in ['cliente', 'administrador']:
                messages.error(request, 'No tienes permiso para acceder.')
                return redirect('inicio')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            usuario = Usuario.objects.get(correo=request.user.username)
            if usuario.rol != 'administrador':
                messages.error(request, 'Solo los administradores pueden acceder.')
                return redirect('inicio')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# ─── VISTAS PUBLICAS ──────────────────────────────────
def inicio(request):
    return render(request, 'index.html', get_contexto(request))

def mascotas(request):
    contexto = get_contexto(request)
    contexto['mascotas'] = Mascota.objects.all()
    return render(request, 'mascotas.html', contexto)

def articulos(request):
    contexto = get_contexto(request)
    contexto['articulos'] = ArticuloInformativo.objects.all()
    return render(request, 'articulos.html', contexto)

def tienda(request):
    contexto = get_contexto(request)
    contexto['productos'] = Producto.objects.filter(disponibilidad__gte=1)
    return render(request, 'tienda.html', contexto)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Correo o contrasena incorrectos.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Las contrasenas no coinciden.')
            return render(request, 'registro.html')

        if User.objects.filter(username=correo).exists() or Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya esta registrado.')
            return render(request, 'registro.html')

        try:
            # Crear User de Django
            user = User.objects.create_user(username=correo, email=correo, password=password)
            user.first_name = nombre
            user.last_name = apellido
            user.save()

            # Crear Usuario personalizado para el carrito
            Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                contraseña_hash='NA',
                rol='cliente',
                fecha_registro=timezone.now(),
                activo=1
            )

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesion.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrio un error: {str(e)}')
            
    return render(request, 'registro.html')

# ─── VISTAS DE CLIENTE ────────────────────────────────
@cliente_required
def carrito(request):
    usuario = get_usuario(request)
    carrito_obj, _ = Carrito.objects.get_or_create(
        usuario_id_usuario=usuario,
        estado='activo',
        defaults={'fecha_creacion': timezone.now()}
    )
    detalles = DetalleCarrito.objects.filter(
        id_carrito=carrito_obj
    ).select_related('id_producto')

    subtotal = sum(d.precio_unitario * d.cantidad for d in detalles)
    impuesto = subtotal * Decimal('0.19')
    envio = Decimal('15000') if subtotal > Decimal('0') else Decimal('0')
    total = subtotal + impuesto + envio

    contexto = get_contexto(request)
    contexto.update({
        'detalles': detalles,
        'subtotal': subtotal,
        'impuesto': impuesto,
        'envio': envio,
        'total': total,
    })
    return render(request, 'carrito.html', contexto)

@cliente_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    usuario = get_usuario(request)
    carrito_obj, _ = Carrito.objects.get_or_create(
        usuario_id_usuario=usuario,
        estado='activo',
        defaults={'fecha_creacion': timezone.now()}
    )
    detalle, created = DetalleCarrito.objects.get_or_create(
        id_carrito=carrito_obj,
        id_producto=producto,
        defaults={'cantidad': 1, 'precio_unitario': producto.precio}
    )
    if not created:
        DetalleCarrito.objects.filter(
            id_carrito=carrito_obj,
            id_producto=producto
        ).update(cantidad=detalle.cantidad + 1)

    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('tienda')

@cliente_required
def eliminar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    usuario = get_usuario(request)
    carrito_obj = Carrito.objects.filter(
        usuario_id_usuario=usuario, estado='activo'
    ).first()
    if carrito_obj:
        DetalleCarrito.objects.filter(
            id_carrito=carrito_obj, id_producto=producto
        ).delete()
    return redirect('carrito')

# ─── VISTAS DE ADMINISTRADOR ─────────────────────────
@admin_required
def admin_productos(request):
    contexto = get_contexto(request)
    contexto['productos'] = Producto.objects.all()
    return render(request, 'admin/productos.html', contexto)

@admin_required
def admin_agregar_producto(request):
    if request.method == 'POST':
        imagen_path = None
        if 'imagen' in request.FILES:
            imagen_file = request.FILES['imagen']
            save_path = os.path.join(settings.BASE_DIR, 'templates', 'img')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            fs = FileSystemStorage(location=save_path)
            filename = fs.save(imagen_file.name, imagen_file)
            imagen_path = f"img/{filename}"

        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            categoria=request.POST.get('categoria'),
            descripcion=request.POST.get('descripcion'),
            precio=request.POST.get('precio'),
            stock=request.POST.get('stock'),
            disponibilidad=1,
            imagen=imagen_path,
            usuario_id_usuario=get_usuario(request)
        )
        messages.success(request, 'Producto agregado correctamente.')
        return redirect('admin_productos')
    return render(request, 'admin/agregar_producto.html', get_contexto(request))

@admin_required
def admin_eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado.')
    return redirect('admin_productos')

@admin_required
def admin_mascotas(request):
    contexto = get_contexto(request)
    contexto['mascotas'] = Mascota.objects.all()
    return render(request, 'admin/mascotas.html', contexto)

@admin_required
def admin_agregar_mascota(request):
    if request.method == 'POST':
        imagen_path = None
        if 'imagen' in request.FILES:
            imagen_file = request.FILES['imagen']
            # Guardamos en templates/img/
            save_path = os.path.join(settings.BASE_DIR, 'templates', 'img')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            fs = FileSystemStorage(location=save_path)
            filename = fs.save(imagen_file.name, imagen_file)
            imagen_path = f"img/{filename}"

        Mascota.objects.create(
            nombre=request.POST.get('nombre'),
            especie=request.POST.get('especie'),
            raza=request.POST.get('raza'),
            edad=request.POST.get('edad'),
            sexo=request.POST.get('sexo'),
            estado_salud=request.POST.get('estado_salud'),
            descripcion=request.POST.get('descripcion'),
            estado_adopcion=request.POST.get('estado_adopcion', 'Disponible'),
            fecha_ingreso=request.POST.get('fecha_ingreso'),
            imagen=imagen_path
        )
        messages.success(request, 'Mascota agregada correctamente.')
        return redirect('admin_mascotas')
    return render(request, 'admin/agregar_mascota.html', get_contexto(request))

@admin_required
def admin_eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
    mascota.delete()
    messages.success(request, 'Mascota eliminada.')
    return redirect('admin_mascotas')

@admin_required
def admin_articulos(request):
    contexto = get_contexto(request)
    contexto['articulos'] = ArticuloInformativo.objects.all()
    return render(request, 'admin/articulos.html', contexto)

@admin_required
def admin_agregar_articulo(request):
    if request.method == 'POST':
        ArticuloInformativo.objects.create(
            titulo=request.POST.get('titulo'),
            categoria=request.POST.get('categoria'),
            contenido=request.POST.get('contenido'),
            fecha_publicacion=request.POST.get('fecha_publicacion'),
            usuario_id_usuario=get_usuario(request)
        )
        messages.success(request, 'Artículo agregado correctamente.')
        return redirect('admin_articulos')
    return render(request, 'admin/agregar_articulo.html', get_contexto(request))

@admin_required
def admin_eliminar_articulo(request, articulo_id):
    articulo = get_object_or_404(ArticuloInformativo, codigo_articulo=articulo_id)
    articulo.delete()
    messages.success(request, 'Artículo eliminado.')
    return redirect('admin_articulos')

# APIS
from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Crear, Leer, Actualizar y eliminar 
def listar_productos(request):
    contexto = get_contexto(request)
    contexto['productos'] = Producto.objects.all()
    return render(request, 'admin/productos.html', contexto)

def crear_producto(request):
    if request.method == 'POST':
        imagen_path = None
        if 'imagen' in request.FILES:
            imagen_file = request.FILES['imagen']
            save_path = os.path.join(settings.BASE_DIR, 'templates', 'img')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            fs = FileSystemStorage(location=save_path)
            filename = fs.save(imagen_file.name, imagen_file)
            imagen_path = f"img/{filename}"

        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            categoria=request.POST.get('categoria'),
            descripcion=request.POST.get('descripcion'),
            precio=request.POST.get('precio'),
            stock=request.POST.get('stock'),
            disponibilidad=1,
            imagen=imagen_path,
            usuario_id_usuario=get_usuario(request)
        )
        messages.success(request, 'Producto agregado correctamente.')
        return redirect('listar')
    return render(request, 'admin/agregar_producto.html', get_contexto(request))

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.categoria = request.POST.get('categoria')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.save()
        messages.success(request, 'Producto editado correctamente.')
        return redirect('listar')
    contexto = get_contexto(request)
    contexto['producto'] = producto
    return render(request, 'admin/agregar_producto.html', contexto)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    producto.delete()
    messages.success(request, 'Producto eliminado.')
    return redirect('listar')


# ─── Asistente MascotasNet 
import google.generativeai as genai
from django.http import JsonResponse
import json

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
modelo = genai.GenerativeModel("models/gemini-2.5-flash")

def chat_ia(request):
    respuesta_ia = None
    error = None
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '')
        try:
            if mensaje:
                respuesta = modelo.generate_content(mensaje)
                respuesta_ia = respuesta.text
        except Exception as e:
            error = str(e)
    return render(request, 'ia.html', {
        'respuesta_ia': respuesta_ia,
        'error': error
    })

def chat_ia_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '')
            if mensaje:
                respuesta = modelo.generate_content(mensaje)
                return JsonResponse({'respuesta_ia': respuesta.text})
            return JsonResponse({'error': 'El mensaje está vacío.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


# ─── SOLICITUDES DE ADOPCION Y PAGOS ──────────────────
@cliente_required
def solicitar_adopcion(request, mascota_id):
    if request.method == 'POST':
        mascota = get_object_or_404(Mascota, id_mascota=mascota_id)
        usuario = get_usuario(request)
        
        # Verificar si ya existe una solicitud pendiente de este usuario para esta mascota
        existe = SolicitudAdopcion.objects.filter(
            usuario_id_usuario=usuario,
            mascota_id_mascota=mascota,
            estado='pendiente'
        ).exists()
        
        if existe:
            messages.warning(request, 'Ya tienes una solicitud pendiente para esta mascota.')
            return redirect('mascotas')
            
        notas = request.POST.get('notas', '')
        
        # Crear la solicitud en la base de datos
        SolicitudAdopcion.objects.create(
            fecha_solicitud=timezone.now().date(),
            estado='pendiente',
            notas=notas,
            usuario_id_usuario=usuario,
            mascota_id_mascota=mascota
        )
        
        # Cambiar el estado de la mascota a "En proceso"
        mascota.estado_adopcion = 'En proceso'
        mascota.save()
        
        messages.success(request, f'Tu solicitud de adopción para {mascota.nombre} ha sido registrada con éxito.')
    return redirect('mascotas')

@cliente_required
def pagar_carrito(request):
    if request.method == 'POST':
        usuario = get_usuario(request)
        carrito_obj = Carrito.objects.filter(
            usuario_id_usuario=usuario,
            estado='activo'
        ).first()
        
        if not carrito_obj:
            messages.error(request, 'No tienes un carrito activo.')
            return redirect('carrito')
            
        detalles = DetalleCarrito.objects.filter(id_carrito=carrito_obj)
        if not detalles.exists():
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('carrito')
            
        # Descontar stock y cerrar carrito
        for d in detalles:
            prod = d.id_producto
            prod.stock = max(0, prod.stock - d.cantidad)
            prod.save()
            
        carrito_obj.estado = 'cerrado'
        carrito_obj.save()
        
        messages.success(request, '¡Pago exitoso! Tu pedido ha sido procesado correctamente.')
    return redirect('carrito')

@admin_required
def admin_solicitudes(request):
    contexto = get_contexto(request)
    contexto['solicitudes'] = SolicitudAdopcion.objects.all().order_by('-fecha_solicitud')
    return render(request, 'admin/solicitudes.html', contexto)

@admin_required
def admin_aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudAdopcion, id_adopcion=solicitud_id)
    solicitud.estado = 'aprobada'
    solicitud.save()
    
    # Actualizar estado de mascota a "Adoptada"
    mascota = solicitud.mascota_id_mascota
    mascota.estado_adopcion = 'Adoptada'
    mascota.save()
    
    messages.success(request, f'La solicitud de adopción de {solicitud.usuario_id_usuario.nombre} para {mascota.nombre} ha sido aprobada.')
    return redirect('admin_solicitudes')

@admin_required
def admin_rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudAdopcion, id_adopcion=solicitud_id)
    solicitud.estado = 'rechazada'
    solicitud.save()
    
    # Si la mascota estaba en proceso, podemos devolverla a "Disponible" si no hay otras solicitudes pendientes
    mascota = solicitud.mascota_id_mascota
    otras_pendientes = SolicitudAdopcion.objects.filter(
        mascota_id_mascota=mascota,
        estado='pendiente'
    ).exclude(id_adopcion=solicitud_id).exists()
    
    if not otras_pendientes:
        mascota.estado_adopcion = 'Disponible'
        mascota.save()
        
    messages.success(request, f'La solicitud de adopción de {solicitud.usuario_id_usuario.nombre} para {mascota.nombre} ha sido rechazada.')
    return redirect('admin_solicitudes')


@cliente_required
def mis_solicitudes(request):
    usuario = get_usuario(request)
    # Solicitudes de adopción
    solicitudes = SolicitudAdopcion.objects.filter(usuario_id_usuario=usuario).select_related('mascota_id_mascota').order_by('-fecha_solicitud')
    
    # Historial de compras (carritos cerrados)
    compras_list = Carrito.objects.filter(usuario_id_usuario=usuario, estado='cerrado').order_by('-fecha_creacion')
    
    # Fetch all details for these carts
    detalles_compras = DetalleCarrito.objects.filter(id_carrito__in=compras_list).select_related('id_producto')
    
    # Group details by cart ID
    detalles_por_carrito = {}
    for detalle in detalles_compras:
        carrito_id = detalle.id_carrito_id
        if carrito_id not in detalles_por_carrito:
            detalles_por_carrito[carrito_id] = []
        detalles_por_carrito[carrito_id].append(detalle)
        
    compras_con_totales = []
    for compra in compras_list:
        detalles = detalles_por_carrito.get(compra.id_carrito, [])
        subtotal = sum(d.precio_unitario * d.cantidad for d in detalles)
        impuesto = subtotal * Decimal('0.19') if subtotal > 0 else Decimal('0')
        envio = Decimal('15000') if subtotal > 0 else Decimal('0')
        total = subtotal + impuesto + envio
        
        compras_con_totales.append({
            'id_carrito': compra.id_carrito,
            'fecha_creacion': compra.fecha_creacion,
            'detalles': detalles,
            'total': total
        })
    
    contexto = get_contexto(request)
    contexto.update({
        'solicitudes': solicitudes,
        'compras': compras_con_totales
    })
    return render(request, 'mis_solicitudes.html', contexto)