import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mascotasnet.settings")
django.setup()

from core.models import Mascota, Producto, ArticuloInformativo

images = {
    'max': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_max_1779205587221.png",
    'luna': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_luna_1779205599647.png",
    'bolita': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_bolita_1779205614252.png",
    'alimento': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_alimento_1779205629269.png",
    'juguete': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_juguete_1779205640385.png",
    'shampoo': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_shampoo_1779205653977.png",
    'articulo': r"C:\Users\HALLER CHAMORRO\.gemini\antigravity\brain\d87c9f80-6887-4992-a3ec-8b73b6a48050\img_articulo_1779205667116.png"
}

dest_dir = r"C:\Users\HALLER CHAMORRO\Desktop\MascotasNet_Django\templates\img"
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

def update_mascota(id_mascota, key):
    m = Mascota.objects.filter(id_mascota=id_mascota).first()
    if m:
        dest_path = os.path.join(dest_dir, f"{key}.png")
        shutil.copy(images[key], dest_path)
        m.imagen = f"img/{key}.png"
        m.save()

def update_producto(id_producto, key):
    p = Producto.objects.filter(id_producto=id_producto).first()
    if p:
        dest_path = os.path.join(dest_dir, f"{key}.png")
        shutil.copy(images[key], dest_path)
        p.imagen = f"img/{key}.png"
        p.save()

def update_articulo(codigo_articulo, key):
    a = ArticuloInformativo.objects.filter(codigo_articulo=codigo_articulo).first()
    if a:
        dest_path = os.path.join(dest_dir, f"{key}.png")
        shutil.copy(images[key], dest_path)
        a.imagen = f"img/{key}.png"
        a.save()

update_mascota(1, 'max')
update_mascota(2, 'luna')
update_mascota(3, 'bolita')

update_producto(1, 'alimento')
update_producto(2, 'juguete')
update_producto(3, 'shampoo')

update_articulo(1, 'articulo')

print("Imágenes copiadas y base de datos actualizada.")
