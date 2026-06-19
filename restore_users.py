import os
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mascotasnet.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Usuario

# 1. Restore the Django user
user_data = {
    'username': 'hallercha@gmail.com',
    'email': 'hallercha@gmail.com',
    'first_name': 'haller',
    'last_name': 'chamorro',
    'password': 'pbkdf2_sha256$1200000$0iDjnnWxDvsFNcRGyqNQMi$4cr9hyPJxBAtkNUQ9L27w55Jbg07Pmd0g5+anJXylto='
}

user, created = User.objects.get_or_create(username=user_data['username'], defaults={'email': user_data['email'], 'first_name': user_data['first_name'], 'last_name': user_data['last_name']})
if created:
    # Update password hash directly since it's already hashed
    User.objects.filter(username=user_data['username']).update(password=user_data['password'])
    print(f"User {user_data['username']} restored in auth_user.")

# 2. Restore the Core user
u, u_created = Usuario.objects.get_or_create(
    correo='hallercha@gmail.com',
    defaults={
        'nombre': 'haller',
        'apellido': 'chamorro',
        'contraseña_hash': 'NA',
        'rol': 'cliente',
        'fecha_registro': timezone.now(),
        'activo': 1
    }
)
if u_created:
    print(f"Usuario {u.correo} restored in core_usuario.")

print("Users restoration completed.")
