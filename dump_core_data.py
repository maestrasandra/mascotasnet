import os
import django
import json
from django.core.serializers import serialize

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mascotasnet.settings")
django.setup()

from core.models import Usuario, Mascota, Producto, ArticuloInformativo, Carrito, DetalleCarrito, SolicitudAdopcion

models_to_dump = [Usuario, Mascota, Producto, ArticuloInformativo, Carrito, DetalleCarrito, SolicitudAdopcion]

with open('backup_core.json', 'w', encoding='utf-8') as f:
    data = []
    for model in models_to_dump:
        serialized_data = serialize('json', model.objects.all())
        data.extend(json.loads(serialized_data))
    
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Datos de core guardados en backup_core.json exitosamente.")
