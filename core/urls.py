from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# APIS
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mascotas/', views.mascotas, name='mascotas'),
    path('tienda/', views.tienda, name='tienda'),
    path('articulos/', views.articulos, name='articulos'),
    path('carrito/', views.carrito, name='carrito'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Recuperación de contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done_complete.html'), name='password_reset_complete'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('admin-panel/productos/', views.admin_productos, name='admin_productos'),
    path('admin-panel/productos/agregar/', views.admin_agregar_producto, name='admin_agregar_producto'),
    path('admin-panel/productos/eliminar/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    
    path('admin-panel/mascotas/', views.admin_mascotas, name='admin_mascotas'),
    path('admin-panel/mascotas/agregar/', views.admin_agregar_mascota, name='admin_agregar_mascota'),
    path('admin-panel/mascotas/eliminar/<int:mascota_id>/', views.admin_eliminar_mascota, name='admin_eliminar_mascota'),
    
    path('admin-panel/articulos/', views.admin_articulos, name='admin_articulos'),
    path('admin-panel/articulos/agregar/', views.admin_agregar_articulo, name='admin_agregar_articulo'),
    path('admin-panel/articulos/eliminar/<int:articulo_id>/', views.admin_eliminar_articulo, name='admin_eliminar_articulo'),

    path('listar/', views.listar_productos, name='listar'),
    path('crear/', views.crear_producto, name='crear'),
    path('editar/<int:id>/', views.editar_producto, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar'),

    path('chat/', views.chat_ia, name='chat_ia'),
    path('chat-api/', views.chat_ia_api, name='chat_ia_api'),

    # Solicitudes de adopción y Pagos
    path('mascotas/solicitar/<int:mascota_id>/', views.solicitar_adopcion, name='solicitar_adopcion'),
    path('carrito/pagar/', views.pagar_carrito, name='pagar_carrito'),
    path('admin-panel/solicitudes/', views.admin_solicitudes, name='admin_solicitudes'),
    path('admin-panel/solicitudes/aprobar/<int:solicitud_id>/', views.admin_aprobar_solicitud, name='admin_aprobar_solicitud'),
    path('admin-panel/solicitudes/rechazar/<int:solicitud_id>/', views.admin_rechazar_solicitud, name='admin_rechazar_solicitud'),

    # APIS
    path('', include(router.urls)),
]